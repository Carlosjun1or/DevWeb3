from funcionario import Funcionario

class FuncionarioComum(Funcionario):
    def __init__(self, nome, valor_hora, horas_trabalhadas):
        super().__init__(nome, valor_hora, horas_trabalhadas)

    def __str__(self):
        return f'Funcionario Comum - {super().__str__()}'