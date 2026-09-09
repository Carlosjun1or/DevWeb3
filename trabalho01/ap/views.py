from django.shortcuts import redirect, render
from .models import Contato, Servico
from .forms import FormContato, FormServico

# Create your views here.

def index(request):
    return render (request, "index.html")

def servicos(request):
    
    servicos = Servico.objects.all()
        
    return render (request, "servicos.html", {'servicos': servicos})

def addServico(request):
    form = FormServico(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('servicos')

    return render (request, "add-servico.html", {'form': form})

def excluirServico(request, id):
    servico = Servico.objects.get(id=id)
    servico.delete()
    return redirect('servicos')

def editarServico(request, id):
    servico = Servico.objects.get(id=id)
    form = FormServico(request.POST or None, request.FILES or None, instance=servico)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('servicos')

    return render (request, "editar-servico.html", {'form': form})

def produtos(request):
    servicos = Servico.objects.all()
    return render(request, "produtos.html", {'servicos': servicos})

def contatos(request):
    contatos = Contato.objects.all()
    return render(request, "contatos.html", {'contatos': contatos})

def novoContato(request):
    if request.method == "POST":
        form = FormContato(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FormContato()
    
    return render(request, "novo-contato.html", {'form': form})

def excluirContato(request, id):
    contato = Contato.objects.get(id=id)
    contato.delete()
    return redirect('contatos')