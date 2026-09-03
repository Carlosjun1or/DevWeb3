from django.shortcuts import redirect, render
from .models import Servico
from .forms import FormServico

# Create your views here.

def index(request):
    return render (request, "index.html")

def servicos(request):
    
    servicos = Servico.objects.all()
        
    return render (request, "servicos.html", {'servicos': servicos})

def addServico(request):
    form = FormServico(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('servicos')

    return render (request, "add-servico.html", {'form': form})

def excluirServico(request, id):
    servico = Servico.objects.get(id=id)
    servico.delete()
    return redirect('servicos')