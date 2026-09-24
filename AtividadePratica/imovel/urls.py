from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro-imovel/', views.add_imovel, name='add_imovel'),
    path('cadastro-corretor/', views.add_corretor, name='add_corretor'),
    path('imovel/', views.imoveis, name='imoveis'),
    path('corretor/', views.corretores, name='corretores'),
    path('edit-imovel/<int:id>/', views.edit_imovel, name='edit_imovel'),
    path('del-imovel/<int:id>/', views.del_imovel, name='del_imovel'),
    path('edit-corretor/<int:id>/', views.edit_corretor, name='edit_corretor'),
    path('del-corretor/<int:id>/', views.del_corretor, name='del_corretor'),
]