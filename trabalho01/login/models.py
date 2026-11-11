from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
    ]

    class Meta:
        app_label = 'login'

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_perfil')

    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')

    def __str__(self):
        return f'Perfil de {self.usuario.username} - {self.tipo_usuario}'