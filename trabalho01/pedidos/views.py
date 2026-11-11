from decimal import Decimal, InvalidOperation

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from catalogo.models import Servico
from .models import Pedido, PedidoItem

CART_SESSION_KEY = 'nimbo_cart'
MAX_QUANTITY = 99


def _cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})
    return cart if isinstance(cart, dict) else {}


def _save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session['nimbo_cart_count'] = sum(
        int(item.get('quantidade', 0))
        for item in cart.values()
        if isinstance(item, dict) and str(item.get('quantidade', '')).isdigit()
    )


def _cart_redirect(request):
    destination = request.POST.get('next') or request.META.get('HTTP_REFERER', '')
    if destination and url_has_allowed_host_and_scheme(
        destination,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(destination)
    return redirect('carrinho')


def _partner_product(product_id):
    try:
        response = requests.get(
            f'https://fakestoreapi.com/products/{product_id}',
            timeout=5,
        )
        response.raise_for_status()
        product = response.json()
    except (requests.RequestException, ValueError):
        return None, 'Não foi possível carregar o produto parceiro. Tente novamente.'

    if not isinstance(product, dict) or product.get('id') != product_id:
        return None, 'O produto parceiro não está disponível para pedido.'

    try:
        price = Decimal(str(product['price'])).quantize(Decimal('0.01'))
    except (KeyError, InvalidOperation, TypeError, ValueError):
        return None, 'Não foi possível validar o preço deste produto parceiro.'

    if not price.is_finite() or price <= 0 or price >= Decimal('100000000'):
        return None, 'O preço deste produto parceiro é inválido.'

    name = str(product.get('title', '')).strip()
    if not name:
        return None, 'O produto parceiro não tem um nome válido.'

    return {
        'tipo': 'partner',
        'id': product_id,
        'nome': name[:255],
        'descricao': str(product.get('description', '')),
        'categoria': str(product.get('category', ''))[:100],
        'imagem': str(product.get('image') or '')[:500],
        'preco': str(price),
        'moeda': 'USD',
    }, None


def _add_to_cart(request, item):
    cart = _cart(request)
    key = f"{item['tipo']}:{item['id']}"
    existing_item = cart.get(key)
    if not isinstance(existing_item, dict):
        existing_item = {}
    current_quantity = existing_item.get('quantidade', 0)
    try:
        current_quantity = int(current_quantity)
    except (TypeError, ValueError):
        current_quantity = 0
    item['quantidade'] = min(current_quantity + 1, MAX_QUANTITY)
    cart[key] = item
    _save_cart(request, cart)


@require_POST
def comprar(request, id):
    service = get_object_or_404(
        Servico.objects.select_related('categoria'),
        pk=id,
        ativo=True,
    )
    _add_to_cart(request, {
        'tipo': 'service',
        'id': service.pk,
        'nome': service.nome,
        'descricao': service.descricao,
        'categoria': service.categoria.nome if service.categoria else '',
        'imagem': service.imagem.url if service.imagem else '',
        'preco': str(service.preco),
        'moeda': 'BRL',
    })
    messages.success(request, f'{service.nome} foi adicionado ao carrinho.')
    return _cart_redirect(request)


@require_POST
def comprar_produto_parceiro(request, id):
    item, error = _partner_product(id)
    if error:
        messages.error(request, error)
        return _cart_redirect(request)

    _add_to_cart(request, item)
    messages.success(request, f'{item["nome"]} foi adicionado ao carrinho.')
    return _cart_redirect(request)


def ver_carrinho(request):
    cart = _cart(request)
    items = []
    totals = {}
    total_quantity = 0
    for key, item in cart.items():
        if not isinstance(item, dict):
            continue
        try:
            quantity = int(item.get('quantidade', 0))
            price = Decimal(str(item.get('preco', '')))
        except (InvalidOperation, TypeError, ValueError):
            continue
        if quantity < 1 or quantity > MAX_QUANTITY or not price.is_finite() or price < 0:
            continue
        currency = item.get('moeda', 'USD' if item.get('tipo') == 'partner' else 'BRL')
        item_with_key = {**item, 'chave': key, 'quantidade': quantity, 'preco_decimal': price}
        items.append(item_with_key)
        total_quantity += quantity
        totals[currency] = totals.get(currency, Decimal('0.00')) + price * quantity

    return render(request, 'carrinho.html', {
        'itens_carrinho': items,
        'quantidade_carrinho': total_quantity,
        'totais_por_moeda': totals,
    })


@require_POST
def atualizar_carrinho(request, tipo, id):
    cart = _cart(request)
    key = f'{tipo}:{id}'
    if key not in cart:
        messages.error(request, 'Esse item não está no carrinho.')
        return redirect('carrinho')
    try:
        quantity = int(request.POST.get('quantidade', ''))
    except (TypeError, ValueError):
        messages.error(request, 'Informe uma quantidade válida.')
        return redirect('carrinho')
    if quantity < 0 or quantity > MAX_QUANTITY:
        messages.error(request, f'A quantidade deve estar entre 0 e {MAX_QUANTITY}.')
        return redirect('carrinho')
    if quantity == 0:
        cart.pop(key)
        messages.success(request, 'Item removido do carrinho.')
    else:
        cart[key]['quantidade'] = quantity
        messages.success(request, 'Carrinho atualizado.')
    _save_cart(request, cart)
    return redirect('carrinho')


@require_POST
def remover_do_carrinho(request, tipo, id):
    cart = _cart(request)
    cart.pop(f'{tipo}:{id}', None)
    _save_cart(request, cart)
    messages.success(request, 'Item removido do carrinho.')
    return redirect('carrinho')


@login_required
@require_POST
def finalizar_compra(request):
    cart = _cart(request)
    if not cart:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')

    validated_items = []
    for item in cart.values():
        if not isinstance(item, dict):
            messages.error(request, 'Há um item inválido no carrinho. Remova-o e tente novamente.')
            return redirect('carrinho')
        item_type = item.get('tipo')
        try:
            product_id = int(item.get('id'))
            quantity = int(item.get('quantidade', 0))
        except (TypeError, ValueError):
            messages.error(request, 'Há um item inválido no carrinho. Remova-o e tente novamente.')
            return redirect('carrinho')
        if quantity < 1 or quantity > MAX_QUANTITY:
            messages.error(request, 'Atualize as quantidades do carrinho antes de finalizar.')
            return redirect('carrinho')

        if item_type == 'service':
            service = Servico.objects.select_related('categoria').filter(
                pk=product_id,
                ativo=True,
            ).first()
            if service is None:
                messages.error(request, 'Um serviço do carrinho não está mais disponível.')
                return redirect('carrinho')
            validated_items.append({
                'tipo': 'service',
                'id': service.pk,
                'servico': service,
                'nome': service.nome,
                'descricao': service.descricao,
                'categoria': service.categoria.nome if service.categoria else '',
                'imagem': service.imagem.url if service.imagem else '',
                'preco': service.preco,
                'moeda': 'BRL',
                'quantidade': quantity,
            })
        elif item_type == 'partner':
            partner_item, error = _partner_product(product_id)
            if error:
                messages.error(request, error)
                return redirect('carrinho')
            partner_item['preco'] = Decimal(partner_item['preco'])
            partner_item['quantidade'] = quantity
            validated_items.append(partner_item)
        else:
            messages.error(request, 'Há um tipo de item inválido no carrinho.')
            return redirect('carrinho')

    with transaction.atomic():
        order = Pedido.objects.create(usuario=request.user)
        PedidoItem.objects.bulk_create([
            PedidoItem(
                pedido=order,
                servico=item.get('servico'),
                produto_parceiro_id=item['id'] if item['tipo'] == 'partner' else None,
                nome=item['nome'],
                descricao=item['descricao'],
                categoria=item['categoria'],
                imagem=item['imagem'],
                quantidade=item['quantidade'],
                preco_unitario=item['preco'],
                moeda=item['moeda'],
            )
            for item in validated_items
        ])

    del request.session[CART_SESSION_KEY]
    request.session['nimbo_cart_count'] = 0
    messages.success(request, 'Pedido finalizado com sucesso. Nenhuma cobrança foi realizada.')
    return redirect('meus_pedidos')


@login_required
def meus_pedidos(request):
    orders = Pedido.objects.filter(usuario=request.user).prefetch_related(
        'items__servico',
    ).order_by('-criado_em')
    for order in orders:
        totals = {}
        for item in order.items.all():
            totals[item.moeda] = totals.get(item.moeda, Decimal('0.00')) + item.subtotal
        if not order.items.exists():
            totals[order.moeda] = order.preco
        order.totais = totals
    return render(request, 'meus_pedidos.html', {
        'pedidos': orders,
    })
