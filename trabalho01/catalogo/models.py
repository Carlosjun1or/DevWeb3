from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='servicos', blank=True, null=True)

    def __str__(self):
        return self.nome
