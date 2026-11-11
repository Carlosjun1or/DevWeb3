from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Perfil


class ContasTests(TestCase):
    def test_admin_routes_are_protected_for_visitors(self):
        response = self.client.get(reverse('contatos_admin'))
        self.assertIn(response.status_code, (302, 403))

    def test_client_can_access_dashboard(self):
        user = get_user_model().objects.create_user(username='cliente', password='senha123')
        Perfil.objects.create(usuario=user, tipo_usuario='cliente')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
