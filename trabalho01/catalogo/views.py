from decimal import Decimal

import requests
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from contas.permissions import admin_required
from .forms import FormServico
from .models import Categoria, Servico
from .serializers import CategoriaSerializer


@admin_required
def servicos(request):
    queryset = Servico.objects.filter(ativo=True)
    busca = request.GET.get('busca')
    categoria = request.GET.get('categoria')
    faixa = request.GET.get('preco')
    ordem = request.GET.get('ordem')

    if busca:
        queryset = queryset.filter(nome__icontains=busca)
    if categoria:
        queryset = queryset.filter(categoria_id=categoria)
    if faixa == 'baixo':
        queryset = queryset.filter(preco__lte=50)
    elif faixa == 'medio':
        queryset = queryset.filter(preco__gt=50, preco__lte=250)
    elif faixa == 'alto':
        queryset = queryset.filter(preco__gt=250)

    if ordem == 'menor':
        queryset = queryset.order_by('preco')
    elif ordem == 'maior':
        queryset = queryset.order_by('-preco')
    elif ordem == 'nome':
        queryset = queryset.order_by('nome')

    categorias = Categoria.objects.filter(ativo=True)
    return render(request, 'servicos.html', {
        'servicos': queryset,
        'categorias': categorias,
        'busca': busca or '',
        'categoria': categoria or '',
        'preco': faixa or '',
        'ordem': ordem or '',
    })


@admin_required
def add_servico(request):
    form = FormServico(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('servicos_admin')
    return render(request, 'add-servico.html', {'form': form})


@admin_required
def editar_servico(request, id):
    servico = get_object_or_404(Servico, pk=id)
    form = FormServico(request.POST or None, request.FILES or None, instance=servico)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('servicos_admin')
    return render(request, 'editar-servico.html', {'form': form, 'servico': servico})


@admin_required
def excluir_servico(request, id):
    if request.method != 'POST':
        raise Http404
    servico = get_object_or_404(Servico, pk=id)
    servico.delete()
    return redirect('servicos_admin')


def produtos(request):
    busca = request.GET.get('q', '').strip()
    tipo_busca = request.GET.get('tipo', 'todos')
    if tipo_busca not in {'todos', 'servicos', 'produtos'}:
        tipo_busca = 'todos'

    servicos = Servico.objects.filter(ativo=True)
    if busca and tipo_busca in {'todos', 'servicos'}:
        servicos = servicos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
        )

    produtos_api = []
    produtos_api_disponivel = False
    if tipo_busca in {'todos', 'produtos'}:
        try:
            response = requests.get('https://fakestoreapi.com/products', timeout=5)
            response.raise_for_status()
            resposta_api = response.json()
            produtos_api = [
                produto for produto in resposta_api
                if isinstance(produto, dict)
            ] if isinstance(resposta_api, list) else []
            produtos_api_disponivel = isinstance(resposta_api, list)
        except (requests.RequestException, ValueError):
            produtos_api = []

        if busca:
            termo = busca.casefold()
            produtos_api = [
                produto for produto in produtos_api
                if termo in ' '.join((
                    str(produto.get('title', '')),
                    str(produto.get('description', '')),
                    str(produto.get('category', '')),
                )).casefold()
            ]

    return render(request, 'produtos.html', {
        'servicos': servicos,
        'produtos_api': produtos_api,
        'busca': busca,
        'tipo_busca': tipo_busca,
        'produtos_api_disponivel': produtos_api_disponivel,
    })


@api_view(['GET', 'POST'])
def categorias_api(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def categoria_api(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    if request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def relatorios(request):
    servicos = Servico.objects.all()
    ativos = servicos.filter(ativo=True).count()
    inativos = servicos.filter(ativo=False).count()
    categorias = servicos.values('categoria__nome').annotate(quantidade=Count('id'))
    return render(request, 'relatorios.html', {
        'total_servicos': servicos.count(),
        'servicos_ativos': ativos,
        'servicos_inativos': inativos,
        'mais_barato': servicos.order_by('preco').first(),
        'mais_caro': servicos.order_by('-preco').first(),
        'categorias_labels': [item['categoria__nome'] or 'Sem categoria' for item in categorias],
        'categorias_valores': [item['quantidade'] for item in categorias],
        'status_valores': [ativos, inativos],
    })
