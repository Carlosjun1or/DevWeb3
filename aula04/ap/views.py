from django.shortcuts import render
from .models import Servico

# Create your views here.

def index(request):
    return render (request, "index.html")

def servicos(request):
    
    servicos = Servico.objects.all()
    
    return render (request, "servicos.html", {'servicos': servicos})
