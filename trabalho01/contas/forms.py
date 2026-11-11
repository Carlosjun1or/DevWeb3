from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')
    first_name = forms.CharField(required=False, label='Nome')
    last_name = forms.CharField(required=False, label='Sobrenome')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
