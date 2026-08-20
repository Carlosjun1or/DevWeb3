from funcionario_comum import FuncionarioComum
from funcionario_especial import FuncionarioEspecial

funcionarios = [
    FuncionarioComum("Fernanda", 25.0, 160),
    FuncionarioEspecial("Felipe", 30.0, 160),
    FuncionarioComum("Carlos", 20.0, 140),
    FuncionarioEspecial("Carolina", 35.0, 150),
]

for f in funcionarios:
    print(f)
    print(f"Pagamento líquido: R${f.calcular_pagamento()}\n")