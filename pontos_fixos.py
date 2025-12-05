
import matplotlib.pyplot as plt
import numpy as np
from typing import *
def flatten(dic:dict):
    aux = {}
    for k, v in dic.items():
        try:
            for k1, v1 in flatten(v.__dict__).items():
                aux[str(v)+'_'+k1]=v1
        except:
            aux[k]=v
    return aux

class pontos:
    def __init__(self, e, s, pr):
        self.e  = e
        self.s  = s
        self.pr = pr
        self.pontos = np.zeros(pr)

    def __str__(self):
        return 'pontos'

    def pontos_uniforme(self):
        self.pontos =  np.linspace(self.e, self.s, self.pr)
    
    def pontos_ciruclar(self):
        from math import cos, pi
        s, e, pr = self.s, self.e, self.pr
        self.pontos = np.array([(1+cos(x*pi/pr))/2 for x in range(pr+1)])

    def pontos_hiper(self):
        pass

    def get_pontos(self):
        return self.pontos.copy()

class counter:
    def __init__(self, n):
        self.c = n
        self.e = 0

    def __str__(self):
        return f'count_{self.c}'

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.c>self.e:
            self.c-=1
            return True
        else:
            raise StopIteration

class base:
    x: np.ndarray
    y: np.ndarray
    a: float        #param da f
    n: int = 1      #n° de composições de f
    c: int = 0      #iterações do método

    def __init__(self, x:pontos, a:float, n:int):
        self.a = a
        self.x = x
        self.y = x.get_pontos()
        self.n = n

    def __str__(self):
        pass

    def get(self, what:str)-> Any | None:
        match what:
            case 'tudo':
                return flatten(self.__dict__)
            case 'graph':
                return self.apply(self.obj, self.x.get_pontos())
            case _:
                return self.__getattribute__(what)
            
    def f(self, x:int|float|np.ndarray)->int|float|np.ndarray:
        pass

    def df(self, x:int|float|np.ndarray)->int|float|np.ndarray:
        pass

    def erro(self):
        pass
    
    def obj(self, x):
        return self.n_iter_f(x) - x
    
    def dx_obj(self, x):
        return self.n_iter_df(x) - 1
    
    def n_iter_(self, f, a):
        return self.apply_while(f, a, counter(self.n))

    def n_iter_f(self, x):
        return self.n_iter_(self.f, x)
    
    def n_iter_df(self, x):
        return self.n_iter_(self.df, x)

    def NM(self, x:int|float|np.ndarray)->int|float|np.ndarray:
        return x - self.obj(x)/self.dx_obj(x)

    def apply(self, f, x:np.ndarray)->np.ndarray:
        return np.apply_along_axis(f, 0, x)
         
    def apply_NM(self, x):
        return self.apply(self.NM, x)        

    def apply_g(self, f:Callable, t:Any, fc:Callable|Iterator)-> Any | None:
        if isinstance(fc, Iterator):
            return self.apply_while(f, t, fc)
        elif isinstance(fc, Callable):
            return self.apply_for(f, t, fc)
        else:
            raise NotImplementedError
        
    def apply_for(self, f:Callable, t:Any, fc:Callable)-> Any | None:
        x = t
        while fc():
            x = f(x)
        return x
    
    def apply_while(self, f:Callable, t:Any, fc:Iterator)-> Any | None:
        x = t
        for _ in fc:
            x = f(x)
        return x

    def apply_g_NM(self, t, fc):
        return self.apply_g(self.apply_NM, t, fc)

class F_da_IC(base):
    def __init__(self, x, n):
        super().__init__(x, None, n)
        self.a = 2.1+5**0.5
        self.delta = None

    def get(self, what):
        if self.delta is None:
            self.delta = self.erro()
        return super().get(what)

    def f(self, x)->float:
        x[x<-1]=-1
        return self.a * x * (1-x)
    
    def df(self, x)->float:
        return self.a - self.a*2*x
    
    def erro(self)->float:
        return sum(self.obj(self.y))*1/self.y.shape[0]
    
    def set_delta(self, d):
        self.delta = d

    def objetiva(self):
        if self.erro()>self.delta:
            self.c+=1
            return True
        return False
    
    def calc(self, c):
        if isinstance(c, int):
            self.c = c
            self.y = self.apply_g_NM(self.y, counter(c))
        else:
            self.set_delta(c)
            self.y = self.apply_g_NM(self.y, self.objetiva)

def calc_plot(obj:base):
    dados = obj.get('tudo')
    coordx = dados['pontos_pontos']
    coordy = dados['y']

    graph = obj.get('graph')  

    plt.scatter(coordy, [0]*len(coordy))
    plt.plot(coordx, graph)
    plt.plot(coordx, [0]*len(coordy))
    # plt.xlim(0,1)
    # plt.ylim(-1.2, 1.2)
    plt.xlabel(f'n_pontos = {dados['pontos_pr']} calcs = {dados['c']}  it = {dados['n']}  delta = {dados['delta']:.2e}')
    plt.show()
    
