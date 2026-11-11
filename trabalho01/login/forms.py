from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Seu nome de usuário', 'autocomplete': 'username'}
        )
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Sua senha', 'autocomplete': 'current-password'}
        )


class CadastroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'voce@exemplo.com',
                'autocomplete': 'email',
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Nome de usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Confirmação de senha',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'Escolha um nome de usuário', 'autocomplete': 'username'}
        )
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Crie uma senha', 'autocomplete': 'new-password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repita sua senha', 'autocomplete': 'new-password'}
        )
