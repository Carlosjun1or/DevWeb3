from django import forms

from .models import Contato


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('nome', 'telefone', 'email', 'mensagem')


class FormIntegrante(forms.Form):
    nome = forms.CharField(max_length=120, label='Nome')
    cargo = forms.CharField(max_length=120, label='Cargo')
    biografia = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        label='Biografia',
    )
    foto_url = forms.URLField(required=False, label='URL da foto')
