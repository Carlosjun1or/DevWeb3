from django.contrib import admin
from .models import Servico, Categoria, Contato

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Contato)
admin.site.register(Servico)