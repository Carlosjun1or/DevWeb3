from django import forms

from .models import Servico


class PrecoBRLField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.strip().replace('R$', '').replace('\xa0', '').replace(' ', '')
            if ',' in value:
                value = value.replace('.', '').replace(',', '.')
        return super().to_python(value)


class FormServico(forms.ModelForm):
    preco = PrecoBRLField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={
                'inputmode': 'decimal',
                'data-mask': 'currency',
                'placeholder': 'R$ 0,00',
                'autocomplete': 'off',
            }
        ),
    )

    class Meta:
        model = Servico
        fields = ('nome', 'descricao', 'preco', 'imagem', 'ativo', 'categoria')
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do serviço'}),
            'descricao': forms.Textarea(
                attrs={'placeholder': 'Descreva o serviço oferecido'}
            ),
        }
