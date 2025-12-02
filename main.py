import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
from os import removedirs, remove, listdir, path, makedirs
from multiprocessing import Pool
from sys import argv, exit


alpha = 2+5**0.5
pr = 1000
imgs = 30
dpi =100
print('='*40)

if len(argv) > 1:
    try:
        alpha = eval(argv[1])
        pr = int(argv[2])
        imgs = int(argv[3])
        dpi = int(argv[4])
        print('>>usando')
        print('>alpha = '+str(alpha)+'\n>imgs  = '+str(imgs)+'\n>trh   = '+str(1)+'\n>pr    = '+str(pr)+'\n>up_s  = '+str(dpi))
    except IndexError:
        raise ValueError('o scrypt toma 4 argumentos: alpha, precisão, n_de_imagens, upscale das imgs')
    except ValueError:
        raise ValueError('os argumentos devem ter tipos float/EA, int, int, int>0')
else:
    print('>>usando defaults')
    print('>alpha = '+str(alpha)+'\n>imgs  = '+str(imgs)+'\n>trh   = '+str(1)+'\n>pr    = '+str(pr)+'\n>up_s  = '+str(dpi))
    

def f(b:float)->float:
    return alpha*b*(1-b)


def n_iter(it, n)->bool:
    while n>=0:
        it = f(it)
        n-=1
        if it>1:
            return False
    return True


def scatter(pr:int, n:int, a:float, s=0, e=1)->tuple[list, list]:
    pontos = [s+x*(e-s)/pr for x in range(pr+2)]
    valores = list(map(lambda x: 1 if n_iter(x, n) else 0, pontos))
    return  pontos, valores, n

    
def saveplot(trab:tuple[list, list], graph:list, pr:int, alpha:float, dpi:int=1)->None:
    pontos, valores, i = trab[0], trab[1], trab[2]
    
    fig, ax = plt.subplots()
    ax.plot(pontos, graph, label='f')
    ax.plot(pontos, pontos)
    ax.plot(pontos, [1]*len(pontos))
    def adder(trab):
        a, b = trab
        if b == False:
            return patches.Rectangle((a-2/pr, 0), 1/pr, 1.2, facecolor='green', alpha=0.5, zorder=-1)
        else:
            return patches.Rectangle((a-2/pr, 0), 1/pr, 1.2, facecolor='red', alpha=0.5, zorder=-1)

    for k in map(adder, zip(pontos, valores)):
        ax.add_patch(k)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel('alpha ='+str(round(alpha, 4))+' n = '+str(i)+' trh = '+str(1)+' pr = '+str(pr)+' dpi = ' + str(100*dpi))
    ax.set_ylabel("Y")
    ax.set_title("Plot dos intervalos de escape para f^"+str(i))
    ax.legend(loc=1)

    plt.savefig(f'temp/{i:003}', dpi=100*dpi)
    
    plt.close()


def namer()->str:
    c = 1
    name = f"output({c}).gif"
    while path.exists(name):
        c+=1
        name = f"output({c}).gif"
    return name

try:
    makedirs('temp')
except FileExistsError:
    print('='*40)
    print('warning: pasta "temp" já existe')
    print('limpar possiveis conteudos da pasta?')
    a = input('y para limpar: ')
    print('='*40)
    if a.strip() == 'y':
        for i in listdir('temp'):
            remove('temp/'+i)
    else: exit()
    
print('='*40)
print('>>calculando gráficos')
trab = [scatter(pr, i, alpha) for i in range(imgs)]
graph = list(map(lambda x: f(x), trab[0][0]))
print('>>gerando artes')

def aux(x:tuple[list, list]):
    saveplot(x, graph=graph, pr=pr, alpha=alpha, dpi=dpi)
with Pool(4) as pool:
    pool.map(aux, trab)


print('>>criando gif')
files = listdir('temp/')
files = sorted(files)
frames:list[Image] = []
for image_path in files:
    img = Image.open('temp/'+image_path)
    frames.append(img)
first_frame:Image = frames[0]
remaining_frames = frames[1:]

name = namer()
print(f'>>salvando <{name}>')
first_frame.save(
    name,
    format="GIF",
    append_images=remaining_frames,
    save_all=True,
    duration=200, # Duration of each frame in milliseconds
    loop=0 # 0 for infinite loop, a number for specific loops
)

for i in files:
    remove('temp/'+i)
removedirs('temp')
print('>>temp limpa')
print(f'>>terminando')
print('='*40)

    
