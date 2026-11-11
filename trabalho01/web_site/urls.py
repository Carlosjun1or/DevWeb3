from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('produtos/', views.produtos, name='produtos'),
    path('contato/', views.contato, name='contato'),
    path('contatos/', views.contatos_admin, name='contatos_admin'),
    path('contatos/<int:id>/excluir/', views.excluir_contato, name='excluir_contato'),
    path('painel/equipe/', views.integrantes_admin, name='integrantes_admin'),
    path('painel/equipe/novo/', views.add_integrante, name='add_integrante'),
    path('painel/equipe/<int:id>/editar/', views.editar_integrante, name='editar_integrante'),
    path('painel/equipe/<int:id>/excluir/', views.excluir_integrante, name='excluir_integrante'),
]
