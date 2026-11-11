from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroForm
from .models import Perfil

CARDS_CLIENTE = [
    {'tag': 'perfil', 'title': 'Editar Perfil', 'text': 'Atualize seus dados pessoais.', 'url': 'perfil_contas'},
    {'tag': 'pedidos', 'title': 'Meus Pedidos', 'text': 'Acompanhe o histórico de suas compras.', 'url': 'meus_pedidos'},
]

CARDS_ADMIN = [
    {'tag': 'perfil', 'title': 'Editar Perfil', 'text': 'Atualize seus dados pessoais.', 'url': 'perfil_contas'},
    {'tag': 'contatos', 'title': 'Contatos', 'text': 'Veja e gerencie mensagens recebidas.', 'url': 'contatos_admin'},
    {'tag': 'servicos', 'title': 'Serviços', 'text': 'Cadastre, edite e filtre serviços.', 'url': 'servicos_admin'},
    {'tag': 'equipe', 'title': 'Equipe', 'text': 'Gerencie os integrantes do time.', 'url': 'integrantes_admin'},
    {'tag': 'relatorios', 'title': 'Relatórios', 'text': 'Acompanhe indicadores e gráficos.', 'url': 'relatorios'},
    {'tag': 'admin', 'title': 'Django Admin', 'text': 'Acesso ao painel administrativo do Django.', 'url': 'admin:index'},
]


@login_required
def dashboard(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user, defaults={'tipo_usuario': 'cliente'})
    cards = CARDS_ADMIN if perfil.tipo_usuario == 'administrador' or request.user.is_staff or request.user.is_superuser else CARDS_CLIENTE
    return render(request, 'dashboard.html', {'cards': cards, 'title': 'Dashboard'})


@login_required
def perfil(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        email = request.POST.get('email', usuario.email)
        if User.objects.filter(email__iexact=email).exclude(pk=usuario.pk).exists():
            messages.error(request, 'Este e-mail já está sendo usado por outro usuário.')
            return render(request, 'perfil.html', {'usuario': usuario})
        usuario.email = email
        usuario.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_contas')

    return render(request, 'perfil.html', {'usuario': request.user})


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()
                Perfil.objects.get_or_create(usuario=usuario, defaults={'tipo_usuario': 'cliente'})
            messages.success(request, 'Usuário cadastrado com sucesso! Agora você pode entrar.')
            return redirect('contas_login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})
