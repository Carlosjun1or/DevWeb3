from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalogo.models import Categoria, Servico
from .models import Pedido, PedidoItem


class PedidosTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='cliente',
            password='senha123',
        )
        self.category = Categoria.objects.create(nome='Tecnologia', ativo=True)
        self.service = Servico.objects.create(
            nome='Website',
            descricao='Site para sua empresa',
            preco='99.90',
            categoria=self.category,
            ativo=True,
        )

    def test_adicionar_servico_guarda_no_carrinho_sem_criar_pedido(self):
        response = self.client.post(reverse('comprar', args=[self.service.pk]))

        self.assertRedirects(response, reverse('carrinho'))
        self.assertFalse(Pedido.objects.exists())
        cart = self.client.session['nimbo_cart']
        self.assertEqual(cart[f'service:{self.service.pk}']['quantidade'], 1)
        cart_page = self.client.get(reverse('carrinho'))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, 'Website')
        self.assertContains(cart_page, 'Entrar para finalizar')

    def test_servico_inativo_nao_pode_ser_adicionado_ao_carrinho(self):
        self.service.ativo = False
        self.service.save(update_fields=['ativo'])

        response = self.client.post(reverse('comprar', args=[self.service.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertNotIn('nimbo_cart', self.client.session)

    @patch('pedidos.views.requests.get')
    def test_adicionar_parceiro_guarda_no_carrinho_sem_criar_pedido(self, get_product):
        get_product.return_value = self.partner_api_response()

        response = self.client.post(reverse('comprar_produto_parceiro', args=[7]))

        self.assertRedirects(response, reverse('carrinho'))
        self.assertFalse(Pedido.objects.exists())
        item = self.client.session['nimbo_cart']['partner:7']
        self.assertEqual(item['nome'], 'Mochila')
        self.assertEqual(item['preco'], '109.95')

    def test_atualizar_quantidade_e_remover_item(self):
        self.client.post(reverse('comprar', args=[self.service.pk]))
        response = self.client.post(
            reverse('atualizar_carrinho', args=['service', self.service.pk]),
            {'quantidade': 3},
        )
        self.assertRedirects(response, reverse('carrinho'))
        self.assertEqual(
            self.client.session['nimbo_cart'][f'service:{self.service.pk}']['quantidade'],
            3,
        )

        self.client.post(reverse('remover_do_carrinho', args=['service', self.service.pk]))
        self.assertEqual(self.client.session['nimbo_cart'], {})

    @patch('pedidos.views.requests.get')
    def test_finalizar_carrinho_misto_cria_um_pedido_com_itens(self, get_product):
        self.client.post(reverse('comprar', args=[self.service.pk]))
        self.client.post(reverse('comprar', args=[self.service.pk]))
        get_product.return_value = self.partner_api_response()
        self.client.post(reverse('comprar_produto_parceiro', args=[7]))
        self.client.force_login(self.user)

        response = self.client.post(reverse('finalizar_compra'), follow=True)

        self.assertEqual(response.status_code, 200)
        order = Pedido.objects.get(usuario=self.user)
        self.assertEqual(order.items.count(), 2)
        service_item = order.items.get(servico=self.service)
        partner_item = order.items.get(produto_parceiro_id=7)
        self.assertEqual(service_item.quantidade, 2)
        self.assertEqual(str(service_item.subtotal), '199.80')
        self.assertEqual(partner_item.moeda, 'USD')
        self.assertEqual(str(partner_item.subtotal), '109.95')
        self.assertEqual(self.client.session.get('nimbo_cart'), None)
        self.assertContains(response, 'Pedido #')
        self.assertContains(response, 'Pedido finalizado com sucesso.')

    def test_finalizar_exige_login_e_preserva_carrinho(self):
        self.client.post(reverse('comprar', args=[self.service.pk]))

        response = self.client.post(reverse('finalizar_compra'))

        self.assertRedirects(
            response,
            f"{reverse('contas_login')}?next={reverse('finalizar_compra')}",
        )
        self.assertFalse(Pedido.objects.exists())
        self.assertIn(f'service:{self.service.pk}', self.client.session['nimbo_cart'])

    @patch('pedidos.views.requests.get')
    def test_falha_na_api_durante_checkout_nao_cria_pedido_nem_esvazia_carrinho(self, get_product):
        from requests import RequestException

        self.client.force_login(self.user)
        get_product.return_value = self.partner_api_response()
        self.client.post(reverse('comprar_produto_parceiro', args=[7]))
        get_product.side_effect = RequestException('API indisponível')

        response = self.client.post(reverse('finalizar_compra'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Pedido.objects.exists())
        self.assertIn('partner:7', self.client.session['nimbo_cart'])
        self.assertContains(response, 'Não foi possível carregar o produto parceiro')

    def test_pedido_salva_totais_separados_por_moeda(self):
        order = Pedido.objects.create(usuario=self.user)
        PedidoItem.objects.create(
            pedido=order,
            servico=self.service,
            nome='Website',
            preco_unitario='99.90',
            moeda='BRL',
        )
        PedidoItem.objects.create(
            pedido=order,
            produto_parceiro_id=7,
            nome='Mochila',
            preco_unitario='109.95',
            moeda='USD',
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('meus_pedidos'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'R$ 99,90')
        self.assertContains(response, 'US$ 109,95')
        self.assertContains(response, 'Pedido #')

    @staticmethod
    def partner_api_response():
        response = Mock()
        response.json.return_value = {
            'id': 7,
            'title': 'Mochila',
            'description': 'Mochila para viagem',
            'category': 'acessórios',
            'image': 'https://example.com/mochila.png',
            'price': 109.95,
        }
        return response
