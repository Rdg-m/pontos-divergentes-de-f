from sys import argv

#parse por argumentos do terminal
if len(argv)>1:
    kargs = dict()
    args = []
    for i in argv:
        if '=' in i:
            aux = i.split('=')
            kargs[aux[0]] = aux[1]
        else:
            args.append(i)
    
def solll(args_list:list, args_var:list=args, kargs:dict=kargs):
    aux = []
    for k, v in kargs.items():
        if k in args_list:
            aux.append((k, v))
            args_list.pop(args_list.index(k))
    return dict(aux+list(zip(args_list, args_var)))

def update_args(vars, *args):
    print('='*40)
    print('caso deseje mudar os valores padrões \nescreva os argumentos na ordem:\n' \
    ">"+str(args)+"\n" \
    "ou de forma alternativa use como kargs\nex: foo=boo")

    for k, v in solll([x for x in args]).items():
        vars[k] = type(vars[k])(v)
    print('='*40)

    for i in args:
        print(f'- {i:<6} <- {vars[i]}')