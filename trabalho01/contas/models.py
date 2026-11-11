from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contas_perfil')
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')

    def __str__(self):
        return f'{self.usuario.username} ({self.tipo_usuario})'
