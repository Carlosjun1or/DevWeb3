from decimal import Decimal
from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Servico


class CatalogoTests(TestCase):
    def test_admin_services_route_is_protected(self):
        response = self.client.get(reverse('servicos_admin'))
        self.assertIn(response.status_code, (302, 403))

    @patch('catalogo.views.requests.get')
    def test_product_search_filters_partner_products(self, get_products):
        response_api = Mock()
        response_api.json.return_value = [
            {
                'id': 1,
                'title': 'Backpack',
                'description': 'A bag for travel',
                'category': 'accessories',
                'image': 'https://example.com/bag.png',
                'price': 25,
            },
            {
                'id': 2,
                'title': 'Notebook',
                'description': 'For school',
                'category': 'electronics',
                'image': 'https://example.com/notebook.png',
                'price': 100,
            },
        ]
        get_products.return_value = response_api

        response = self.client.get(
            reverse('produtos'),
            {'q': 'BACKPACK', 'tipo': 'produtos'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['title'] for item in response.context['produtos_api']], ['Backpack'])
        self.assertEqual(response.context['busca'], 'BACKPACK')
        self.assertEqual(response.context['tipo_busca'], 'produtos')
        self.assertEqual(response.context['servicos'].count(), 0)
        get_products.assert_called_once()

    @patch('catalogo.views.requests.get')
    def test_product_search_filters_services_by_category_without_api(self, get_products):
        categoria = Categoria.objects.create(nome='Identidade visual')
        Servico.objects.create(
            nome='Pacote de marca',
            descricao='Criação de identidade para sua empresa.',
            preco=Decimal('150.00'),
            ativo=True,
            categoria=categoria,
        )
        Servico.objects.create(
            nome='Desenvolvimento web',
            descricao='Site responsivo para sua marca.',
            preco=Decimal('300.00'),
            ativo=True,
        )

        response = self.client.get(
            reverse('produtos'),
            {'q': 'identidade', 'tipo': 'servicos'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['servicos'].values_list('nome', flat=True)),
            ['Pacote de marca'],
        )
        self.assertEqual(response.context['produtos_api'], [])
        get_products.assert_not_called()
