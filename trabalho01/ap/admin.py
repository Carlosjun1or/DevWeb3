from django.contrib import admin
from .models import Categoria, Contato, Servico

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "descricao")
    ordering = ("nome",)
    list_per_page = 25


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone")
    search_fields = ("nome", "email", "telefone", "mensagem")
    ordering = ("nome",)
    list_per_page = 25


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "categoria", "preco", "ativo", "criado_em")
    list_filter = ("categoria", "ativo")
    search_fields = ("nome", "descricao", "categoria__nome")
    ordering = ("nome", "preco")
    date_hierarchy = "criado_em"
    list_per_page = 25