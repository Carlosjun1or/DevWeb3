from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo_usuario")
    list_filter = ("tipo_usuario",)
    search_fields = ("usuario__username", "usuario__email")
    ordering = ("usuario__username",)
    list_per_page = 25
