from django.urls import path

from . import views

urlpatterns = [
    path('comprar/<int:id>/', views.comprar, name='comprar'),
    path('comprar-produto-parceiro/<int:id>/', views.comprar_produto_parceiro, name='comprar_produto_parceiro'),
    path('carrinho/', views.ver_carrinho, name='carrinho'),
    path('carrinho/atualizar/<str:tipo>/<int:id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('carrinho/remover/<str:tipo>/<int:id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
]
