from django.contrib.auth import get_user_model
from django.core import mail
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

    def test_cadastro_valido_redireciona_com_mensagem_de_sucesso(self):
        response = self.client.post(
            reverse('cadastro_contas'),
            {
                'username': 'novocliente',
                'first_name': 'Novo',
                'last_name': 'Cliente',
                'email': 'novo.cliente@exemplo.com',
                'password1': 'SenhaForte-987!',
                'password2': 'SenhaForte-987!',
            },
            follow=True,
        )
        self.assertEqual(response.redirect_chain, [(reverse('contas_login'), 302)])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário cadastrado com sucesso! Agora você pode entrar.')
        self.assertTrue(get_user_model().objects.filter(username='novocliente').exists())

    def test_cadastro_invalido_exibe_mensagem_de_erro(self):
        response = self.client.post(
            reverse('cadastro_contas'),
            {
                'username': 'usuario_ruim',
                'email': 'email_invalido',
                'password1': '123',
                'password2': '456',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Não foi possível concluir o cadastro. Verifique os campos destacados.')
        self.assertFalse(get_user_model().objects.filter(username='usuario_ruim').exists())

    def test_recuperacao_senha_envia_email_com_link_de_redefinicao(self):
        user = get_user_model().objects.create_user(
            username='usuario_reset',
            email='usuario_reset@exemplo.com',
            password='senhaAntiga123!',
        )
        response = self.client.post(
            reverse('password_reset'),
            {'email': 'usuario_reset@exemplo.com'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('usuario_reset@exemplo.com', mail.outbox[0].to)
        self.assertIn('/contas/reset/', mail.outbox[0].body)

        # Extrair link gerado no e-mail e redefinir a senha
        import re
        match = re.search(r'http://testserver(/contas/reset/[^ \n]+)', mail.outbox[0].body)
        self.assertIsNotNone(match)
        reset_url = match.group(1)

        # GET no link de redefinição segue o redirecionamento de sessão interna do Django
        get_confirm = self.client.get(reset_url, follow=True)
        self.assertEqual(get_confirm.status_code, 200)

        # POST definindo a nova senha
        post_confirm = self.client.post(
            get_confirm.request['PATH_INFO'],
            {
                'new_password1': 'NovaSenhaSegura-2026!',
                'new_password2': 'NovaSenhaSegura-2026!',
            },
            follow=True,
        )
        self.assertEqual(post_confirm.status_code, 200)
        self.assertRedirects(post_confirm, reverse('password_reset_complete'))

        # Validar que a senha foi alterada com sucesso
        user.refresh_from_db()
        self.assertTrue(user.check_password('NovaSenhaSegura-2026!'))
