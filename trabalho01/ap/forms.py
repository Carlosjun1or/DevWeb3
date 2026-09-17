from django import forms
from .models import Contato, Servico

class FormServico(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ("nome", "descricao", "preco", "imagem", "ativo", "categoria")
        
class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ("nome", "email", "telefone", "mensagem")