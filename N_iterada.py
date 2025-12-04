import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


class ABC:
    pr:int
    dpi:int
    imgs:int
    alpha:float

    def __init__(self, pr, n):
        self.alpha = 2+5**0.5+0.00001
        self.pr = pr
        self.n = n

    def __str__(self, a=None):
        if a is not None: return f'f^{a} com {self.pr} pontos'
        return f'f^{self.n} com {self.pr} pontos'

    def f(self, x:float)->float:
        pass
    
    def n_iter(self, x:float)->float:
        pass
        
    def plot(self)->None:
        pass



class N_iterada(ABC):
    resultado:np.ndarray #não deve ser alterado após exec
    iterações:int = 0
    def __init__(self, n, pr, alpha=None):
        super().__init__(pr, n)
        self.resultado = None
        if alpha is not None:
            self.alpha = alpha

    def __str__(self):
        return super().__str__(self.iterações) 

    def get_result(self):
        return self.resultado.copy()
    
    def make_patch(self, s, e):
        #cria um retangulo entre Start e End
        return patches.Rectangle((s, 0), (e-s), 2, facecolor='#F99999', alpha=1, zorder=-1)
    def make_patch_simetrico(self, x, t):
        #cria um retangulo entre Start e End
        return patches.Rectangle((x-t/2, 0), t, 2, facecolor='#F99999', alpha=1, zorder=-1)


    def plot(self):
        print(f'>criando plot n({self.iterações})', end='')
        fig, ax = plt.subplots()
    
        #acha um cobertura ótima para os intervalos
        #n>12 vai ter muito poucos intervalos:
        #       deixo de aplicar o mesmo filtro
        if self.iterações<12:
            dados, singularities = self.mask_for_low_n()
            for y in singularities:
                #adiciona barras de len == 1
                ax.add_patch(
                    self.make_patch_simetrico(
                        y-1/self.pr, 
                        1/self.pr)
                    )
            #adiciona os retangulos ao gráfico
            for x in range(1,len(dados[0]), 2): 
                ax.add_patch(
                    self.make_patch(
                        dados[0,x-1], 
                        dados[0, x]))
                
        else:
            dados = self.mask_for_high_n()
            for i in range(len(dados[1,:])):
                ax.add_patch(
                    self.make_patch_simetrico(
                        dados[0,i], 
                        1/self.pr)
                    )


        #BOILER de MATPLOT
        ax.set_facecolor("#AFF288")
        ax.set_xlim(min(self.resultado[0, :]), max(self.resultado[0, :]))
        ax.set_ylim(0, 1)
        ax.set_xlabel('alpha ='+str(round(self.alpha, 3))+' n = '+str(self.iterações)+' trh = 1'+' pr = '+str(self.pr) )
        ax.set_ylabel("Y")
        ax.set_title("Plot dos intervalos de escape para f^"+str(self.iterações))

        #ver se aux funciona como esperado
        # plt.plot(aux[0,:], aux[1,:])
        #plotar gráfico de f e de x=1
        ax.plot(self.resultado[0, :], np.apply_along_axis(self.f, 0, self.resultado[0, :]))


    def plot_show(self):
        self.plot()
        plt.show()

    def plot_save(self, dpi, pathname):
        self.plot()
        plt.savefig(pathname, dpi=100*dpi)
        plt.close()

    def f(self, x):
        x[x<-1]=-1 #prevenção de underflow
        return self.alpha * x * (1-x)
    
    def n_iter(self, x):
        #n°ésima iteração de f
        n = self.n
        while n>0:
            x = self.f(x)
            n-=1
        return x
    
    def mask_for_low_n(self):
        #gera uma mascara no numpy
        # 1 == ficou em [0, 1]
        # 0 == saiu
        dados = self.get_result()
        dados[1,:][np.bitwise_and(dados[1,:]<=1, dados[1,:]>=0)] = 1
        dados[1,:][dados[1,:]!=1]=0

        filtro, singu = self.filtro(dados)

        return dados[:,filtro], singu
    
    def mask_for_high_n(self):
        #gera uma mascara no numpy
        # 1 == ficou em [0, 1]
        # 0 == saiu
        dados = self.get_result()
        dados[1,:][np.bitwise_and(dados[1,:]<=1, dados[1,:]>=0)] = 1
        dados[1,:][dados[1,:]!=1]=0

        dados = dados[:,dados[1,:]==1]

        return dados
        
    def filtro(self, serie):
        sig, y = serie[1,:], serie[0,:]
        lst = [True]
        singularities = []
        for i in range(1, len(sig)-1):
            if sig[i-1]==0 and sig[i]==1 and sig[i+1]==0:
                singularities.append(y[i])
                lst.append(False)
            elif sig[i-1]==1 and sig[i]==1 and sig[i+1]==0:
                lst.append(True)
            elif sig[i-1]==0 and sig[i]==1 and sig[i+1]==1:
                lst.append(True)
            else:
                lst.append(False)
        lst.append(True)
        return np.array(lst), singularities
        

    def exec(self, s, e):
        self.iterações +=self.n
        #faz a distribuição regular de pr+1 pontos no intervalo [s, e]
        pr = self.pr
        if not isinstance(self.resultado, np.ndarray):
            aux = np.array([s+x*(e-s)/pr for x in range(pr+1)])
            aux = np.stack([aux,np.apply_along_axis(self.n_iter, 0, aux)])
        else:
            #calcula o resultado dos pontos usando numpy
            aux = self.resultado
            aux = np.stack([aux[0,:], np.apply_along_axis(self.n_iter, 0, self.resultado[1,:])])

        #salva no objeto como var privada
        self.resultado = aux

    def criar_n_imagens(self, n, dpi, path):
        for i in range(n):
            #itera n vezes
            self.exec(0, 1)
            # self.plot_show()
            self.plot_save(dpi,path+f'/{i:003}')
            print(f'|> salvo como {i:003}.png')
