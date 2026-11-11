from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import CadastroForm
from .models import Perfil


class ContasTests(TestCase):
    def test_registration_form_displays_placeholders(self):
        form = CadastroForm()

        self.assertEqual(
            form.fields['username'].widget.attrs['placeholder'],
            'Escolha um nome de usuário',
        )
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'voce@exemplo.com')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Crie uma senha')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Repita sua senha')

    def test_login_form_displays_input_placeholders(self):
        response = self.client.get(reverse('contas_login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'placeholder="Seu nome de usuário"')
        self.assertContains(response, 'placeholder="Sua senha"')

    def test_admin_routes_are_protected_for_visitors(self):
        response = self.client.get(reverse('contatos_admin'))
        self.assertIn(response.status_code, (302, 403))

    def test_client_can_access_dashboard(self):
        user = get_user_model().objects.create_user(username='cliente', password='senha123')
        Perfil.objects.create(usuario=user, tipo_usuario='cliente')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
