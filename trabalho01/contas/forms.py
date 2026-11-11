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
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'voce@exemplo.com',
                'autocomplete': 'email',
            }
        ),
    )
    first_name = forms.CharField(
        required=False,
        label='Nome',
        widget=forms.TextInput(
            attrs={'placeholder': 'Seu nome', 'autocomplete': 'given-name'}
        ),
    )
    last_name = forms.CharField(
        required=False,
        label='Sobrenome',
        widget=forms.TextInput(
            attrs={'placeholder': 'Seu sobrenome', 'autocomplete': 'family-name'}
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
