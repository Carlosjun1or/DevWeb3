import json
import logging
from decimal import Decimal
from pathlib import Path

import requests
from django.db.models import Avg, Count, F, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from contas.permissions import admin_required
from pedidos.models import Pedido, PedidoItem
from .forms import FormServico
from .models import Categoria, Servico
from .serializers import CategoriaSerializer

logger = logging.getLogger(__name__)
MOCK_PRODUCTS_FILE = Path(__file__).resolve().parent / 'mock_produtos.json'


def _load_mock_products():
    if MOCK_PRODUCTS_FILE.exists():
        try:
            with open(MOCK_PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception as e:
            logger.warning('Failed to load mock products: %s', e)
    return []


@admin_required
def servicos(request):
    queryset = Servico.objects.all()
    busca = request.GET.get('busca')
    categoria = request.GET.get('categoria')
    faixa = request.GET.get('preco')
    ordem = request.GET.get('ordem')

    if busca:
        queryset = queryset.filter(nome__icontains=busca)
    if categoria:
        queryset = queryset.filter(categoria_id=categoria)
    if faixa == 'baixo':
        queryset = queryset.filter(preco__lte=1000)
    elif faixa == 'medio':
        queryset = queryset.filter(preco__gt=1000, preco__lte=2000)
    elif faixa == 'alto':
        queryset = queryset.filter(preco__gt=2500)

    if ordem == 'menor':
        queryset = queryset.order_by('preco')
    elif ordem == 'maior':
        queryset = queryset.order_by('-preco')
    elif ordem == 'nome':
        queryset = queryset.order_by('nome')

    categorias = Categoria.objects.all()
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

    servicos = Servico.objects.all()
    if busca and tipo_busca in {'todos', 'servicos'}:
        servicos = servicos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(categoria__nome__icontains=busca)
        )

    produtos_api = []
    produtos_api_disponivel = False
    if tipo_busca in {'todos', 'produtos'}:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/125.0.0.0 Safari/537.36'
            ),
            'Accept': 'application/json',
        }
        try:
            response = requests.get('https://fakestoreapi.com/products', headers=headers, timeout=5)
            response.raise_for_status()
            resposta_api = response.json()
            if isinstance(resposta_api, list) and len(resposta_api) > 0:
                produtos_api = [p for p in resposta_api if isinstance(p, dict)]
                produtos_api_disponivel = True
            else:
                produtos_api = _load_mock_products()
                produtos_api_disponivel = len(produtos_api) > 0
        except (requests.RequestException, ValueError) as err:
            logger.info('FakeStoreAPI unavailable (%s), using local fallback.', err)
            produtos_api = _load_mock_products()
            produtos_api_disponivel = len(produtos_api) > 0

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


@admin_required
def relatorios(request):
    visao = request.GET.get('visao', 'todos')
    if visao not in {'todos', 'vendas', 'servicos'}:
        visao = 'todos'

    context = {
        'visao': visao,
    }

    # Relatórios de Serviços
    if visao in {'todos', 'servicos'}:
        servicos = Servico.objects.all()
        ativos = servicos.filter(ativo=True).count()
        inativos = servicos.filter(ativo=False).count()
        total = servicos.count()
        categorias = (
            servicos.values('categoria__nome')
            .annotate(quantidade=Count('id'))
            .order_by('-quantidade', 'categoria__nome')
        )
        top_servicos = servicos.order_by('-preco', 'nome')[:5]
        media_preco = servicos.aggregate(media=Avg('preco'))['media']

        context.update({
            'total_servicos': total,
            'servicos_ativos': ativos,
            'servicos_inativos': inativos,
            'percentual_ativos': round(ativos / total * 100) if total else 0,
            'total_categorias': Categoria.objects.count(),
            'preco_medio': media_preco,
            'mais_barato': servicos.order_by('preco').first(),
            'mais_caro': servicos.order_by('-preco').first(),
            'categorias_labels': [item['categoria__nome'] or 'Sem categoria' for item in categorias],
            'categorias_valores': [item['quantidade'] for item in categorias],
            'status_labels': ['Ativos', 'Inativos'],
            'status_valores': [ativos, inativos],
            'top_servicos_labels': [servico.nome for servico in top_servicos],
            'top_servicos_valores': [float(servico.preco) for servico in top_servicos],
        })

    # Relatórios de Vendas / Pedidos
    if visao in {'todos', 'vendas'}:
        pedidos = Pedido.objects.prefetch_related('items__servico')
        total_pedidos = pedidos.count()
        total_clientes = pedidos.values('usuario').distinct().count()

        # Itens e faturamento
        itens_pedidos = PedidoItem.objects.select_related('pedido', 'servico')
        total_itens_vendidos = sum(item.quantidade for item in itens_pedidos)

        faturamento_brl = Decimal('0.00')
        faturamento_usd = Decimal('0.00')

        # Se houver itens na tabela PedidoItem
        if itens_pedidos.exists():
            for item in itens_pedidos:
                sub = item.subtotal
                if item.moeda == 'USD':
                    faturamento_usd += sub
                else:
                    faturamento_brl += sub
        else:
            # Caso existam pedidos legados sem PedidoItem
            for pedido in pedidos:
                if pedido.moeda == 'USD':
                    faturamento_usd += pedido.preco
                else:
                    faturamento_brl += pedido.preco

        # Tipos de produto vendidos
        itens_servico_count = sum(item.quantidade for item in itens_pedidos if item.servico_id is not None)
        itens_parceiro_count = sum(item.quantidade for item in itens_pedidos if item.servico_id is None)

        # Produtos mais vendidos (top 5 por quantidade total)
        top_produtos_agg = (
            PedidoItem.objects.values('nome')
            .annotate(total_qtd=Sum('quantidade'))
            .order_by('-total_qtd', 'nome')[:5]
        )
        top_produtos_labels = [p['nome'] for p in top_produtos_agg]
        top_produtos_valores = [p['total_qtd'] for p in top_produtos_agg]

        # Top clientes (com mais pedidos)
        top_clientes_agg = (
            Pedido.objects.values('usuario__username', 'usuario__first_name')
            .annotate(qtd_pedidos=Count('id'))
            .order_by('-qtd_pedidos')[:5]
        )
        top_clientes_labels = [
            c['usuario__first_name'] or c['usuario__username']
            for c in top_clientes_agg
        ]
        top_clientes_valores = [c['qtd_pedidos'] for c in top_clientes_agg]

        ticket_medio_brl = (faturamento_brl / total_pedidos) if total_pedidos > 0 else Decimal('0.00')

        context.update({
            'total_pedidos': total_pedidos,
            'total_clientes': total_clientes,
            'total_itens_vendidos': total_itens_vendidos,
            'faturamento_brl': faturamento_brl,
            'faturamento_usd': faturamento_usd,
            'ticket_medio_brl': ticket_medio_brl,
            'itens_servico_count': itens_servico_count,
            'itens_parceiro_count': itens_parceiro_count,
            'tipo_vendas_labels': ['Serviços Nimbo', 'Produtos Parceiros'],
            'tipo_vendas_valores': [itens_servico_count, itens_parceiro_count],
            'top_produtos_labels': top_produtos_labels,
            'top_produtos_valores': top_produtos_valores,
            'top_clientes_labels': top_clientes_labels,
            'top_clientes_valores': top_clientes_valores,
        })

    return render(request, 'relatorios.html', context)
