#dados salvos n podem ser editados ou excluidos, somente consultados

# coordenadas = (10,20) #tupla
# print(coordenadas)

tupla=("verde","amarelo","azul","verde")
print(tupla[2])

# tupla[2]="cinza" #tuplas são imutáveis, não é possível alterar o valor de um elemento

print(len(tupla))
print(tupla.count("verde")) #qts vezes o elemento aparece
print(tupla.index("verde")) #retorna o indice do elemento

if "verde" in tupla:
    print("verde esta na tupla")
else:
    print("verde n esta na tupla")