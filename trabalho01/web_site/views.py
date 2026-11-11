import logging

import httpx
from postgrest import APIError
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalogo.models import Servico
from contas.permissions import admin_required
from .forms import FormContato, FormIntegrante
from .models import Contato
from .supabase_client import (
    SupabaseConfigurationError,
    get_supabase,
    get_supabase_admin,
    supabase_admin_configured,
)

logger = logging.getLogger(__name__)
SUPABASE_ERRORS = (APIError, httpx.HTTPError, SupabaseConfigurationError)


def _team_page_error(request, template, context, operation, error):
    logger.error('Supabase %s failed (%s).', operation, type(error).__name__)
    messages.error(
        request,
        'Não foi possível concluir a operação com a equipe no Supabase. '
        'Verifique a configuração e tente novamente.',
    )
    return render(request, template, {
        **context,
        'supabase_disponivel': supabase_admin_configured(),
    })


def home(request):
    return render(request, 'home.html')


def quem_somos(request):
    try:
        response = (
            get_supabase()
            .table('integrantes')
            .select('id, nome, cargo, biografia, foto_url')
            .order('id')
            .execute()
        )
    except SUPABASE_ERRORS as error:
        logger.error('Could not load team from Supabase (%s).', type(error).__name__)
        return render(request, 'quem_somos.html', {
            'integrantes': [],
            'supabase_disponivel': False,
        })
    return render(request, 'quem_somos.html', {
        'integrantes': response.data or [],
        'supabase_disponivel': True,
    })


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
    try:
        response = (
            get_supabase_admin()
            .table('integrantes')
            .select('id, nome, cargo, biografia, foto_url')
            .order('id')
            .execute()
        )
    except SUPABASE_ERRORS as error:
        return _team_page_error(
            request,
            'integrantes_admin.html',
            {'integrantes': []},
            'team listing',
            error,
        )
    return render(request, 'integrantes_admin.html', {
        'integrantes': response.data or [],
        'supabase_disponivel': True,
    })


@admin_required
def add_integrante(request):
    form = FormIntegrante(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            response = (
                get_supabase_admin()
                .table('integrantes')
                .insert(form.cleaned_data)
                .select('id')
                .execute()
            )
        except SUPABASE_ERRORS as error:
            return _team_page_error(
                request,
                'add_integrante.html',
                {'form': form},
                'team insert',
                error,
            )
        if not response.data:
            logger.error('Supabase team insert returned no inserted row.')
            return _team_page_error(
                request,
                'add_integrante.html',
                {'form': form},
                'team insert confirmation',
                RuntimeError('Supabase did not return the inserted team member.'),
            )
        messages.success(request, 'Integrante cadastrado no Supabase.')
        return redirect('integrantes_admin')
    return render(request, 'add_integrante.html', {
        'form': form,
        'supabase_disponivel': supabase_admin_configured(),
    })


@admin_required
def editar_integrante(request, id):
    try:
        response = (
            get_supabase_admin()
            .table('integrantes')
            .select('id, nome, cargo, biografia, foto_url')
            .eq('id', id)
            .execute()
        )
    except SUPABASE_ERRORS as error:
        return _team_page_error(
            request,
            'editar_integrante.html',
            {'integrante': None},
            'team lookup',
            error,
        )
    integrante = next(iter(response.data or []), None)
    if integrante is None:
        raise Http404('Integrante não encontrado.')

    form = FormIntegrante(request.POST or None, initial=integrante)
    if request.method == 'POST' and form.is_valid():
        try:
            updated = (
                get_supabase_admin()
                .table('integrantes')
                .update(form.cleaned_data)
                .eq('id', id)
                .select('id')
                .execute()
            )
        except SUPABASE_ERRORS as error:
            return _team_page_error(
                request,
                'editar_integrante.html',
                {'integrante': integrante, 'form': form},
                'team update',
                error,
            )
        if not updated.data:
            raise Http404('Integrante não encontrado.')
        messages.success(request, 'Integrante atualizado no Supabase.')
        return redirect('integrantes_admin')
    return render(request, 'editar_integrante.html', {
        'integrante': integrante,
        'form': form,
        'supabase_disponivel': supabase_admin_configured(),
    })


@admin_required
@require_POST
def excluir_integrante(request, id):
    try:
        deleted = (
            get_supabase_admin()
            .table('integrantes')
            .delete()
            .eq('id', id)
            .select('id')
            .execute()
        )
    except SUPABASE_ERRORS as error:
        return _team_page_error(
            request,
            'integrantes_admin.html',
            {'integrantes': []},
            'team deletion',
            error,
        )
    if not deleted.data:
        raise Http404('Integrante não encontrado.')
    messages.success(request, 'Integrante removido do Supabase.')
    return redirect('integrantes_admin')
