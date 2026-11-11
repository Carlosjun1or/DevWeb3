from django import forms

from .models import Contato


class TelefoneInput(forms.TextInput):
    input_type = 'tel'


class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('nome', 'telefone', 'email', 'mensagem')
        widgets = {
            'nome': forms.TextInput(
                attrs={'placeholder': 'Seu nome completo', 'autocomplete': 'name'}
            ),
            'telefone': TelefoneInput(
                attrs={
                    'inputmode': 'numeric',
                    'data-mask': 'phone',
                    'maxlength': '20',
                    'placeholder': '(11) 99999-9999',
                    'autocomplete': 'tel',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'voce@exemplo.com',
                    'autocomplete': 'email',
                }
            ),
            'mensagem': forms.Textarea(
                attrs={'placeholder': 'Como podemos ajudar?'}
            ),
        }


class FormIntegrante(forms.Form):
    nome = forms.CharField(
        max_length=120,
        label='Nome',
        widget=forms.TextInput(
            attrs={'placeholder': 'Nome completo', 'autocomplete': 'name'}
        ),
    )
    cargo = forms.CharField(
        max_length=120,
        label='Cargo',
        widget=forms.TextInput(attrs={'placeholder': 'Ex.: Designer'}),
    )
    biografia = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Conte um pouco sobre o integrante'}
        ),
        label='Biografia',
    )
    foto_url = forms.URLField(
        required=False,
        label='URL da foto',
        widget=forms.URLInput(
            attrs={
                'placeholder': 'https://exemplo.com/foto.jpg',
                'inputmode': 'url',
            }
        ),
    )
