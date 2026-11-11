from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from catalogo.models import Servico


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name='pedidos',
        blank=True,
        null=True,
    )
    produto_parceiro_id = models.PositiveIntegerField(blank=True, null=True)
    produto_nome = models.CharField(max_length=255, blank=True)
    produto_descricao = models.TextField(blank=True)
    produto_categoria = models.CharField(max_length=100, blank=True)
    produto_imagem = models.URLField(max_length=500, blank=True)
    moeda = models.CharField(max_length=3, default='BRL')
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.pk} - {self.usuario.username}'


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name='itens_pedidos',
        blank=True,
        null=True,
    )
    produto_parceiro_id = models.PositiveIntegerField(blank=True, null=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    imagem = models.CharField(max_length=500, blank=True)
    quantidade = models.PositiveSmallIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    moeda = models.CharField(max_length=3, default='BRL')

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f'{self.quantidade} × {self.nome}'
