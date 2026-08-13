#os dados n podem ser repetidos

conjunto={"louro","jose","braga","jose"} #mantem somente o ultimo elemento repetido
print(conjunto)

conjunto.add("ana")

print(conjunto,"\n")

conjunto2={1,2,3}
conjunto.update(conjunto,conjunto2) #adiciona elementos de outro conjunto
print(conjunto,"\n")

conjunto.remove("ana") #remove elemento 
print(conjunto)
print(len(conjunto)) #qtd de elementos do conjunto

for elemento in conjunto: #percorre o conjunto e imprime
    print(elemento)

if "jose" in conjunto: #procura um elemento no conjunto
    print("jose esta no conjunto")
else:
    print("jose n esta no conjunto")

