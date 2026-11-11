from django.db import models


class Contato(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField()
    telefone = models.CharField(max_length=30, blank=True)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
