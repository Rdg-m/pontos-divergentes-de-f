
from arquivo_handling import manejo_arqs, criar_gif
from input_handling   import update_args
from N_iterada        import N_iterada


# ==== PARAMETROS ==============
path = './pngstemp_A&1(s21gi73' 
alpha = 2.1+5**0.5              
pr = 1000                       
imgs = 10                       
dpi = 2                         
n = 1                           
# ==============================

def main():

    #suporte para terminal
    update_args(globals(), 'path', 'alpha', 'pr', 'imgs', 'dpi', 'n')
    FUNC_PRINCIPAL = N_iterada(n, pr)

    #criar pastas e evitar conflitos
    manejo_arqs(path, 'a')
    print('>>main')
    FUNC_PRINCIPAL.criar_n_imagens(imgs, dpi, path)

    #carrega imagens 
    # e cria gif
    criar_gif(path)

    #limpar as pngs
    manejo_arqs(path)

    
if __name__ == '__main__':
    main()
