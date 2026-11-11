from django.urls import path

from . import views

urlpatterns = [
    path('servicos/', views.servicos, name='servicos_admin'),
    path('servicos/novo/', views.add_servico, name='add_servico'),
    path('servicos/<int:id>/editar/', views.editar_servico, name='editar_servico'),
    path('servicos/<int:id>/excluir/', views.excluir_servico, name='excluir_servico'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('produtos/', views.produtos, name='produtos'),
    path('api/categorias/', views.categorias_api, name='categorias_api'),
    path('api/categorias/<int:id>/', views.categoria_api, name='categoria_api'),
]
