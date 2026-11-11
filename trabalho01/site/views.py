from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalogo.models import Servico
from contas.permissions import admin_required
from .forms import FormContato
from .models import Contato
from .supabase_client import get_supabase


def home(request):
    return render(request, 'home.html')


def quem_somos(request):
    supabase = get_supabase()
    integrantes = []
    if supabase:
        try:
            response = supabase.table('integrantes').select('*').execute()
            integrantes = response.data or []
        except Exception:
            integrantes = []
    return render(request, 'quem_somos.html', {'integrantes': integrantes, 'supabase_disponivel': bool(supabase)})


def produtos(request):
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'produtos.html', {'servicos': servicos, 'produtos_api': []})


def contato(request):
    if request.method == 'POST':
        form = FormContato(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem enviada com sucesso! Em breve nossa equipe entrará em contato.')
            return redirect('contato')
    else:
        form = FormContato()
    return render(request, 'contato.html', {'form': form})


@admin_required
def contatos_admin(request):
    contatos = Contato.objects.all().order_by('-id')
    return render(request, 'contatos_admin.html', {'contatos': contatos})


@admin_required
@require_POST
def excluir_contato(request, id):
    contato = get_object_or_404(Contato, pk=id)
    contato.delete()
    messages.success(request, 'Contato removido com sucesso.')
    return redirect('contatos_admin')


@admin_required
def integrantes_admin(request):
    supabase = get_supabase()
    integrantes = []
    if supabase:
        try:
            response = supabase.table('integrantes').select('*').execute()
            integrantes = response.data or []
        except Exception:
            integrantes = []
    return render(request, 'integrantes_admin.html', {'integrantes': integrantes, 'supabase_disponivel': bool(supabase)})


@admin_required
def add_integrante(request):
    supabase = get_supabase()
    if request.method == 'POST' and supabase:
        payload = {
            'nome': request.POST.get('nome'),
            'cargo': request.POST.get('cargo'),
            'biografia': request.POST.get('biografia'),
            'foto_url': request.POST.get('foto_url'),
        }
        supabase.table('integrantes').insert(payload).execute()
        return redirect('integrantes_admin')
    return render(request, 'add_integrante.html', {'supabase_disponivel': bool(supabase)})


@admin_required
def editar_integrante(request, id):
    supabase = get_supabase()
    integrante = None
    if supabase:
        response = supabase.table('integrantes').select('*').eq('id', id).execute()
        integrante = (response.data or [{}])[0]
    if request.method == 'POST' and supabase:
        payload = {
            'nome': request.POST.get('nome'),
            'cargo': request.POST.get('cargo'),
            'biografia': request.POST.get('biografia'),
            'foto_url': request.POST.get('foto_url'),
        }
        supabase.table('integrantes').update(payload).eq('id', id).execute()
        return redirect('integrantes_admin')
    return render(request, 'editar_integrante.html', {'integrante': integrante, 'supabase_disponivel': bool(supabase)})


@admin_required
@require_POST
def excluir_integrante(request, id):
    supabase = get_supabase()
    if supabase:
        supabase.table('integrantes').delete().eq('id', id).execute()
    return redirect('integrantes_admin')
