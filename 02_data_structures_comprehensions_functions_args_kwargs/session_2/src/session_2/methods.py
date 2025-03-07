#def cenas (a:str,b:float,c:bool=False):
#    pass

def cenas(a,b,c=None,*args):
    print(type(args))
    print(type(kwargs))
    print(a,b,c,*args)

a= "ola"
b=3.14
c=True
ar = (1,2,3,4)

cenas(a,b,c,*ar)
