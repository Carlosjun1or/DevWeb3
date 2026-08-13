# frutas = ["maçã", "banana", "laranja", "uva", "pera"]
# print(frutas)

lista = ["Ana",10,9.9,True]
print(lista)

lista[0] = ""
print(lista)

lista.append("48") #add elemento no final
lista.insert(0,"carlos") #add elemento no indice
lista.remove("") #remove o elemento com conteudo igual
lista.pop(2) #remove elemento por indice

print(lista,"\n")

listaNum = [5,2,9,10,3]
listaNum.sort() #ordena a lista
listaNum.reverse() #ordena de forma reversa
print(listaNum)
listaNum.clear() #limpa a lista
print(len(listaNum),"\n") #imprime qnt de elementos na lista

lista2= ["ana","maria","braga"]

for item in lista2: #percorre a lista e imprime
    print(item)

if "mariaa" in lista2: #procura um elemento na lista
    print("maria esta na lista")
else:
    print("maria n esta na lista")


