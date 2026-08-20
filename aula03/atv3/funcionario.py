class Funcionario:

    taxa = 0.10

    def __init__(self, nome, valor_hora, horas_trabalhadas):
        self.nome = nome
        self.valor_hora = valor_hora
        self.horas_trabalhadas = horas_trabalhadas

    def __str__(self):
        return f'Nome: {self.nome} | Valor/Hora: R${self.valor_hora} | Horas: {self.horas_trabalhadas}'

    def salario_bruto(self):
        return self.valor_hora * self.horas_trabalhadas

    def calcular_pagamento(self):
        bruto = self.salario_bruto()
        return bruto - (bruto * self.taxa)