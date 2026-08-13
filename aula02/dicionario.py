# organizado no formato chave:valor

aluno = {
    "nome":"jogo",
    "idade":20,
    "altura":1.75
}

print(aluno) #acessa o dicionario completo
print(aluno["nome"],"\n") #acessa o valor da chave

aluno["curso"] = "dsm" #adiciona um novo elemento no dicionario
aluno["idade"] = 21 #altera o valor de um elemento do dicionario
print(aluno,"\n")

print(aluno.keys()) #imprime as chaves do dicionario
print(aluno.values()) #imprime os valores do dicionario
print(aluno.items()) #imprime os pares chave-valor do dicionario

for chave in aluno.keys(): #percorre o dicionario e imprime as chaves
    print(chave)
    
for valor in aluno.values(): #percorre o dicionario e imprime os valores
    print(valor)
    
for chave,valor in aluno.items(): #percorre o dicionario e imprime os pares chave-valor
    print(chave," : ",valor)
    
if "dsm" in aluno.values(): #procura por valor
    print("dsm esta no dicionario")
else:
    print("dsm n esta no dicionario")