class Pessoa:
    
    ano = 2026
    
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def __str__(self):
        return f'Nome: {self.nome} | Idade: {self.idade}'

    def dtNascimento(self):
        return self.ano - self.idade