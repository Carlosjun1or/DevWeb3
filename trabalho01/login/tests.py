from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Perfil


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
