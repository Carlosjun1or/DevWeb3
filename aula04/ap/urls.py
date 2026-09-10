from django.urls import path 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("servicos", views.servicos, name="servicos"),
    path("add-servico", views.addServico, name="addServico"),
    path("excluir-servico/<int:id>", views.excluirServico, name="excluirServico"),
    path("editar-servico/<int:id>", views.editarServico, name="editarServico"),
]
