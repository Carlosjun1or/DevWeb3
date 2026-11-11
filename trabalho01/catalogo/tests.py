from decimal import Decimal
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import FormServico
from .models import Categoria, Servico


class CatalogoTests(TestCase):
    def test_service_form_accepts_brazilian_currency(self):
        form = FormServico(
            data={
                'nome': 'Serviço de teste',
                'descricao': 'Descrição',
                'preco': 'R$ 1.234,56',
                'ativo': 'on',
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['preco'], Decimal('1234.56'))

    def test_service_form_exposes_currency_mask_and_placeholders(self):
        form = FormServico()

        self.assertEqual(form.fields['preco'].widget.attrs['data-mask'], 'currency')
        self.assertEqual(form.fields['preco'].widget.attrs['placeholder'], 'R$ 0,00')
        self.assertEqual(form.fields['nome'].widget.attrs['placeholder'], 'Nome do serviço')
        self.assertEqual(
            form.fields['descricao'].widget.attrs['placeholder'],
            'Descreva o serviço oferecido',
        )

    def test_admin_services_route_is_protected(self):
        response = self.client.get(reverse('servicos_admin'))
        self.assertIn(response.status_code, (302, 403))

    def test_internal_service_list_includes_inactive_services(self):
        admin = get_user_model().objects.create_user(
            username='catalog-admin',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(admin)
        Servico.objects.create(nome='Serviço ativo', preco=Decimal('10.00'), ativo=True)
        Servico.objects.create(nome='Serviço pausado', preco=Decimal('20.00'), ativo=False)

        response = self.client.get(reverse('servicos_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serviço ativo')
        self.assertContains(response, 'Serviço pausado')
        self.assertContains(response, 'Disponível')
        self.assertContains(response, 'Indisponível')

    @patch('catalogo.views.requests.get')
    def test_public_service_list_shows_inactive_without_purchase_action(self, get_products):
        active_service = Servico.objects.create(
            nome='Serviço disponível',
            preco=Decimal('10.00'),
            ativo=True,
        )
        inactive_service = Servico.objects.create(
            nome='Serviço pausado',
            preco=Decimal('20.00'),
            ativo=False,
        )

        response = self.client.get(reverse('produtos'), {'tipo': 'servicos'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serviço disponível')
        self.assertContains(response, 'Serviço pausado')
        self.assertContains(response, 'Serviço indisponível')
        self.assertContains(
            response,
            reverse('comprar', args=[active_service.pk]),
        )
        self.assertNotContains(
            response,
            reverse('comprar', args=[inactive_service.pk]),
        )
        get_products.assert_not_called()

    def test_reports_show_catalog_metrics_and_chart_data(self):
        categoria = Categoria.objects.create(nome='Design')
        Servico.objects.create(
            nome='Identidade visual',
            preco=Decimal('120.00'),
            ativo=True,
            categoria=categoria,
        )
        Servico.objects.create(
            nome='Site institucional',
            preco=Decimal('450.00'),
            ativo=False,
            categoria=categoria,
        )
        Servico.objects.create(nome='Consultoria', preco=Decimal('80.00'), ativo=True)

        response = self.client.get(reverse('relatorios'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_servicos'], 3)
        self.assertEqual(response.context['servicos_ativos'], 2)
        self.assertEqual(response.context['servicos_inativos'], 1)
        self.assertEqual(response.context['percentual_ativos'], 67)
        self.assertEqual(response.context['preco_medio'], Decimal('216.666666666667'))
        self.assertEqual(response.context['categorias_labels'], ['Design', 'Sem categoria'])
        self.assertEqual(response.context['categorias_valores'], [2, 1])
        self.assertEqual(response.context['status_valores'], [2, 1])
        self.assertEqual(
            response.context['top_servicos_labels'],
            ['Site institucional', 'Identidade visual', 'Consultoria'],
        )
        self.assertContains(response, 'categoriaChart')
        self.assertContains(response, 'statusChart')
        self.assertContains(response, 'precoChart')

    def test_reports_render_when_catalog_is_empty(self):
        response = self.client.get(reverse('relatorios'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_servicos'], 0)
        self.assertEqual(response.context['percentual_ativos'], 0)
        self.assertIsNone(response.context['preco_medio'])
        self.assertContains(response, 'Nenhum serviço cadastrado')
        self.assertContains(response, 'Cadastre serviços para comparar os preços.')

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
