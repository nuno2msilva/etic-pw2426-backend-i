#
def main():
    my_list: list[float] = [...] # A list of float numbers (decimals)
    my_set: set[float] = [...] # A set of float numbers (no repeats)
    my_tuple: tuple[float] = (...) # a immutable iterable, a tuple, rare specimen
    my_dict: dict[str,float] = {'a':1.0} # a dictionary with strings and key


    def add_to_list(value):
        my_list.append(2)

    my_tuple.__add__(2)
    add_to_list(2)
    print(my_tuple)

if __name__ == "__main__":
    main()

def main2(a:str,b:int,c:bool=False):
    ...

lista = []

for i in range(10):
    lista.append(i) # append = push

nova_lista = [number for number in range(10)]
nova_lista_even = [number for number in range(100) if number % 2 is 0]
nova_tuple_even = (number for number in range(100) if number % 2 is 0)
nova_set_even = {number for number in range(100) if number % 2 is 0}
nova_dict_even = {index: number for index, number in range(100) if number %  2 is 0}

nova_set_even [0:3]
nova_set_

for i in range(100):
    if i %2 is 0:
        nova_lista_even.append(i)
print(lista)
print(nova_lista)


