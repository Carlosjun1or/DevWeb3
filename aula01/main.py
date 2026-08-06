"""
from datetime import date

#variaveis
nome = "João"
idade = 15
altura = 1.75
ativo = True
nota = float("8.5") #conversão de string para float
matricula,aluno,curso = 1,"Felipe", "DSM" #funciona atribuição de multiplas variáveis, mas não é recomendado

#comando de saída de dados
print("Olá Mundo!")

print("Tipo do nome: ", type(nome)) #concatenação de strings 
print("Nome: ",nome)
 
print("Nota: ",nota," - Tipo de nota: ", type(nota))

print(f'Matricula: {matricula} - Aluno: {aluno} - Curso: {curso}') #f-string : interpolação de variáveis dentro de uma string

nome = str(input("Digite seu nome: ")) #entrada de dados do usuário, padrao string
idade = int(input("Digite sua idade: "))
nasc = date.today().year - idade #calculo do ano de nascimento
habilitado = True if input("Você é habilitado? (s/n): ").lower() == "s" else False #condicional ternário

print(f'Olá {nome}, vc nasceu em {nasc} e tem {idade} anos. Seja bem-vindo(a) ao curso de Python!')

if date.today().year - nasc >= 60: #esturutura condicional if/elif/else
    print("Você é veio!")
elif date.today().year - nasc>=18 and habilitado: # operadores logicos and/or/not
    print("Você é maior de idade e habilitado!")
elif date.today().year - nasc >= 18:
    print("Você é maior de idade!")
else:
    print("Você é menor de idade!")

"""

import funcao #importando o arquivo funcao.py com todas as funções usando funcao.nome_da_funcao()
from funcao import quadrado #importando só função quadrado() do arquivo funcao.py
 
#LOOP (while/for)
contador = 1

while contador <= 5: #serve para gerar uma repetição de codigo qnd for verdadeiro
    print(" - ",contador, " - ")
    contador += 1
    funcao.saudacao("Carol") # chamada da função saudacao() do arquivo funcao.py
print("Fim do loop while!")

for i in range(5): #serve para coleções de dados / range(1,5) gera uma lista de 1 a 4
    print(" - ",i, " - ")
    print(i,"x",i,"=",quadrado(i)) #chamada da função quadrado() do arquivo funcao.py ou funcao.quadrado(i)