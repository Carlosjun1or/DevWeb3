from django.db import models

# Create your models here.

class Corretor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class TipoImovel(models.TextChoices):
    CASA = 'Casa', 'Casa'
    APARTAMENTO = 'Apartamento', 'Apartamento'
    TERRENO = 'Terreno', 'Terreno'
    
    def __str__(self):
        return self.label
    
class Imovel(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=TipoImovel.choices)
    finalidade = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    quantidade_quartos = models.IntegerField()
    imagem = models.ImageField(upload_to='imoveis/', blank=True, null=True)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    data_cadastro = models.DateTimeField(auto_now_add=True)
