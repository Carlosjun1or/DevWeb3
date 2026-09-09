from django.db import models

# Create your models here.
class Servico(models.Model):
    nome = models.CharField(max_length=100)  
    descricao = models.TextField(blank=True)  
    preco = models.DecimalField(max_digits=10, decimal_places=2)  
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True) 
    ativo = models.BooleanField(default=True)   
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    mensagem = models.TextField() 
    
    def __str__(self):
        return self.nome