from django.shortcuts import redirect, render
from .models import Contato, Servico
from .forms import FormContato, FormServico

# Create your views here.

def index(request):
    return render (request, "index.html")

def servicos(request):
    
    ## servicos = Servico.objects.all()
    servicos = Servico.objects.filter(ativo=True)
    servicos = servicos.exclude(preco=0)   
     
    total_servicos = servicos.count()
    tem_servicos = servicos.exists()
    
    mais_barato = servicos.order_by('preco').first()
    mais_caro = servicos.order_by('-preco').first()
    
    
    #recupera o valor do formulário de busca enviado pelo usuário
    busca = request.GET.get('busca')
    if busca:
        servicos = servicos.filter(nome__icontains=busca)
    
    contexto = {
        'servicos': servicos,
        'total_servicos': total_servicos,
        'tem_servicos': tem_servicos,
        'mais_barato': mais_barato,
        'mais_caro': mais_caro,
        'busca': busca,
    }
        
    return render (request, "servicos.html", contexto)

def addServico(request):
    form = FormServico(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('servicos')

    return render (request, "add-servico.html", {'form': form})

def excluirServico(request, id):
    servico = Servico.objects.get(id=id)
    servico.imagem.delete(save=False)
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