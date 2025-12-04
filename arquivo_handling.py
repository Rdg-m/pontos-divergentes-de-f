from os import remove, listdir, makedirs, path
from PIL import Image
from sys import exit

def criar_gif(path):
    first_frame, remaining_frames = carregar_imgs(path) 
    name = namer()
    print('>>criando gif')
    first_frame.save(
        name,
        format="GIF",
        append_images=remaining_frames,
        save_all=True,
        duration=270, # Duration of each frame in milliseconds
        loop=0 # 0 for infinite loop, a number for specific loops
    )

def namer()->str:
    c = 1
    name = f"output({c}).gif"
    while path.exists(name):
        c+=1
        name = f"output({c}).gif"
    print(f'>>nome: {name}')
    return name

def carregar_imgs(path):
    print('>>carregando imagens')
    files = listdir(path)
    files = sorted(files)
    frames = []
    for image_name in files:
        img = Image.open(path+'/'+image_name)
        frames.append(img)
    return frames[0], frames[1:]

def limpar_pasta(path):
    a = input('y para limpar e continuar\nx para continuar sem limpar: ')
    match a.strip():
        case 'y':
            for i in listdir(path):
                remove(path+'/'+i)
        case 'x':
            pass
        case _:
            exit()
        
def manejo_arqs(path, s:str='o'):
    print('='*40)
    if s == 'a':
        try:
            makedirs(path)
            print(f'>>pasta {path} criada')
        except FileExistsError:
            print('!! pasta "temp" já existe')
            print('   limpar possiveis conteudos da pasta?')
            limpar_pasta(path)
    else:
        print('limpar pngs da pasta?')
        limpar_pasta(path)
    print('='*40)