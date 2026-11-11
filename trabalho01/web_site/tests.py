from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import FormContato, FormIntegrante
from web_site.models import Contato


class SiteTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_user(
            username='admin',
            password='senha-segura-123',
            is_staff=True,
        )

    def test_contact_and_team_forms_include_placeholders_and_phone_mask(self):
        contact_form = FormContato()
        team_form = FormIntegrante()

        self.assertEqual(
            contact_form.fields['telefone'].widget.attrs['data-mask'],
            'phone',
        )
        self.assertEqual(contact_form.fields['telefone'].widget.input_type, 'tel')
        self.assertEqual(
            contact_form.fields['telefone'].widget.attrs['placeholder'],
            '(11) 99999-9999',
        )
        self.assertEqual(
            contact_form.fields['email'].widget.attrs['placeholder'],
            'voce@exemplo.com',
        )
        self.assertEqual(
            team_form.fields['foto_url'].widget.attrs['placeholder'],
            'https://exemplo.com/foto.jpg',
        )

    def test_contato_publico_funciona(self):
        response = self.client.post(reverse('contato'), {
            'nome': 'Carlos',
            'telefone': '11999999999',
            'email': 'carlos@email.com',
            'mensagem': 'Mensagem de teste',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contato.objects.filter(email='carlos@email.com').exists())

    @patch('web_site.views.get_supabase')
    def test_quem_somos_carrega_integrantes_do_supabase(self, get_supabase):
        supabase = Mock()
        supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
            {
                'id': 1,
                'nome': 'Pessoa teste',
                'cargo': 'Design',
                'biografia': 'Biografia de teste',
                'foto_url': '',
            },
        ]
        get_supabase.return_value = supabase

        response = self.client.get(reverse('quem_somos'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['integrantes']), 1)
        self.assertContains(response, 'Pessoa teste')

    @patch('web_site.views.get_supabase_admin')
    def test_painel_lista_integrantes_do_supabase(self, get_supabase_admin):
        self.client.force_login(self.admin)
        supabase = Mock()
        supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
            {
                'id': 8,
                'nome': 'Pessoa teste',
                'cargo': 'Design',
                'biografia': 'Biografia de teste',
                'foto_url': '',
            },
        ]
        get_supabase_admin.return_value = supabase

        response = self.client.get(reverse('integrantes_admin'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pessoa teste')
        self.assertTrue(response.context['supabase_disponivel'])

    @patch('web_site.views.get_supabase_admin')
    def test_admin_adiciona_integrante_no_supabase(self, get_supabase_admin):
        self.client.force_login(self.admin)
        supabase = Mock()
        supabase.table.return_value.insert.return_value.select.return_value.execute.return_value.data = [
            {'id': 8},
        ]
        get_supabase_admin.return_value = supabase
        payload = {
            'nome': 'Pessoa teste',
            'cargo': 'Design',
            'biografia': 'Biografia de teste',
            'foto_url': '',
        }

        response = self.client.post(reverse('add_integrante'), payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('integrantes_admin'))
        supabase.table.assert_called_once_with('integrantes')
        supabase.table.return_value.insert.assert_called_once_with(payload)

    @patch('web_site.views.get_supabase_admin')
    def test_admin_edita_integrante_no_supabase(self, get_supabase_admin):
        self.client.force_login(self.admin)
        supabase = Mock()
        row = {
            'id': 8,
            'nome': 'Pessoa antiga',
            'cargo': 'Design',
            'biografia': 'Biografia antiga',
            'foto_url': '',
        }
        execute = supabase.table.return_value.select.return_value.eq.return_value.execute
        execute.return_value.data = [row]
        supabase.table.return_value.update.return_value.eq.return_value.select.return_value.execute.return_value.data = [
            {'id': 8},
        ]
        get_supabase_admin.return_value = supabase
        payload = {
            'nome': 'Pessoa atualizada',
            'cargo': 'Direção',
            'biografia': 'Nova biografia',
            'foto_url': '',
        }

        response = self.client.post(reverse('editar_integrante', args=[8]), payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('integrantes_admin'))
        supabase.table.return_value.update.assert_called_once_with(payload)

    @patch('web_site.views.get_supabase_admin')
    def test_admin_remove_integrante_do_supabase(self, get_supabase_admin):
        self.client.force_login(self.admin)
        supabase = Mock()
        supabase.table.return_value.delete.return_value.eq.return_value.select.return_value.execute.return_value.data = [
            {'id': 8},
        ]
        get_supabase_admin.return_value = supabase

        response = self.client.post(reverse('excluir_integrante', args=[8]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('integrantes_admin'))
        supabase.table.return_value.delete.assert_called_once_with()

    @patch('web_site.views.supabase_admin_configured', return_value=False)
    def test_admin_form_avisa_que_a_chave_secreta_e_obrigatoria(self, _configured):
        self.client.force_login(self.admin)

        response = self.client.get(reverse('add_integrante'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SUPABASE_SECRET_KEY')
