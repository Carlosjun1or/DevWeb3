from funcionario import Funcionario

class FuncionarioEspecial(Funcionario):

    adicional = 0.20

    def __init__(self, nome, valor_hora, horas_trabalhadas):
        super().__init__(nome, valor_hora, horas_trabalhadas)

    def __str__(self):
        return f'Funcionario Especial - {super().__str__()}'

    def calcular_pagamento(self):
        bruto = self.salario_bruto()
        bruto_com_adicional = bruto + (bruto * self.adicional)
        return bruto_com_adicional - (bruto_com_adicional * self.taxa)