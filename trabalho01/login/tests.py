from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import CadastroForm, LoginForm
from .models import Perfil


class FormPlaceholderTests(TestCase):
    def test_login_and_registration_forms_display_placeholders(self):
        login_form = LoginForm()
        registration_form = CadastroForm()

        self.assertEqual(
            login_form.fields['username'].widget.attrs['placeholder'],
            'Seu nome de usuário',
        )
        self.assertEqual(
            login_form.fields['password'].widget.attrs['placeholder'],
            'Sua senha',
        )
        self.assertEqual(
            registration_form.fields['email'].widget.attrs['placeholder'],
            'voce@exemplo.com',
        )
        self.assertEqual(
            registration_form.fields['password1'].widget.attrs['placeholder'],
            'Crie uma senha',
        )
        self.assertEqual(
            registration_form.fields['password2'].widget.attrs['placeholder'],
            'Repita sua senha',
        )


class CadastroViewTests(TestCase):
    def test_get_exibe_formulario_sem_mensagem_de_sucesso(self):
        response = self.client.get(reverse("cadastrar_usuario"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastro.html")
        self.assertContains(response, "Cadastrar usuário")
        self.assertNotContains(response, "Usuário cadastrado com sucesso!")

    def test_cadastro_valido_cria_usuario_e_redireciona_para_login(self):
        response = self.client.post(
            reverse("cadastrar_usuario"),
            {
                "username": "novo_usuario",
                "email": "novo@example.com",
                "password1": "UmaSenha-Forte-987!",
                "password2": "UmaSenha-Forte-987!",
            },
            follow=True,
        )

        self.assertEqual(response.redirect_chain, [(reverse("login"), 302)])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuário cadastrado com sucesso!")
        usuario = User.objects.get(username="novo_usuario")
        self.assertEqual(usuario.email, "novo@example.com")
        self.assertTrue(Perfil.objects.filter(usuario=usuario, tipo_usuario="cliente").exists())

    def test_cadastro_invalido_mostra_erros_e_nao_cria_usuario(self):
        response = self.client.post(
            reverse("cadastrar_usuario"),
            {
                "username": "usuario_invalido",
                "email": "invalido@example.com",
                "password1": "senha",
                "password2": "diferente",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cadastro.html")
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Não foi possível concluir o cadastro")
        self.assertContains(
            response,
            str(response.context["form"].errors["password2"][0]),
        )
        self.assertFalse(User.objects.filter(username="usuario_invalido").exists())
        self.assertFalse(Perfil.objects.exists())


class DashboardViewTests(TestCase):
    def test_dashboard_exibe_pagina_para_cliente(self):
        usuario = User.objects.create_user(username="cliente", password="senha-forte")
        Perfil.objects.create(usuario=usuario, tipo_usuario="cliente")
        self.client.force_login(usuario)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_dashboard_cria_perfil_cliente_quando_nao_existe(self):
        usuario = User.objects.create_user(username="sem_perfil", password="senha-forte")
        self.client.force_login(usuario)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        perfil = Perfil.objects.get(usuario=usuario)
        self.assertEqual(perfil.tipo_usuario, "cliente")

    def test_dashboard_redireciona_administrador_para_admin(self):
        usuario = User.objects.create_user(
            username="administrador",
            password="senha-forte",
            is_staff=True,
        )
        Perfil.objects.create(usuario=usuario, tipo_usuario="administrador")
        self.client.force_login(usuario)

        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(response, reverse("admin:index"))
