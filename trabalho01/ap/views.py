from django.db.models.aggregates import Count
from django.http import Http404
from django.shortcuts import redirect, render
from .serializers import CategoriaSerializer
from .models import Contato, Servico, Categoria
from .forms import FormContato, FormServico
from .supabase_client import supabase
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

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
        
    #recupera as categorias ativas para exibir no filtro
    categorias = Categoria.objects.filter(ativo=True)
    
    #recupera o valor do filtro de categoria enviado pelo usuário
    categoria = request.GET.get('categoria')
    if categoria:
        #aplica o filtro de categoria aos serviços
        servicos = servicos.filter(categoria_id=categoria)
        
    preco = request.GET.get('preco')
    if preco == 'baixo':
        servicos = servicos.filter(preco__lte=50)
    elif preco == 'medio':
        servicos = servicos.filter(preco__gt=50, preco__lte=250)
    elif preco == 'alto':
        servicos = servicos.filter(preco__gt=250)
    
    ordem = request.GET.get('ordem')
    if ordem == 'menor':
        servicos = servicos.order_by('preco')
    elif ordem == 'maior':
        servicos = servicos.order_by('-preco')
    elif ordem == 'nome':
        servicos = servicos.order_by('nome')

    contexto = {
        'servicos': servicos,
        'total_servicos': total_servicos,
        'tem_servicos': tem_servicos,
        'mais_barato': mais_barato,
        'mais_caro': mais_caro,
        'busca': busca,
        'categoria': categoria,
        'categorias': categorias,
        'preco': preco,
        'ordem' : ordem,
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
    
    resposta = requests.get('https://fakestoreapi.com/products')
    produtos_api = resposta.json()
    return render(request, "produtos.html", {'produtos': servicos, 'produtos_api': produtos_api})

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

def integrantes(request):
    from .supabase_client import supabase

    resposta = (supabase.table("integrantes").select("*").execute())
    return render(request, "integrantes.html", {'integrantes': resposta.data}   )

def addIntegrante(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        cargo = request.POST.get("cargo")
        biografia = request.POST.get("biografia")
        foto_url = request.POST.get("foto_url")
        
        supabase.table("integrantes").insert({
            "nome": nome,
            "cargo": cargo,
            "biografia": biografia,
            "foto_url": foto_url
        }).execute()
        
        return redirect('integrantes')
    
    return render(request, "add-integrante.html")

def editarIntegrante(request, id):
    resposta = supabase.table("integrantes").select("*").eq("id", id).execute()
    if not resposta.data:
        raise Http404("Integrante não encontrado.")

    integrante = resposta.data[0]
    if request.method == "POST":
        supabase.table("integrantes").update({
            "nome": request.POST.get("nome"),
            "cargo": request.POST.get("cargo"),
            "biografia": request.POST.get("biografia"),
            "foto_url": request.POST.get("foto_url"),
        }).eq("id", id).execute()
        return redirect("integrantes")

    return render(request, "editar-integrante.html", {"integrante": integrante})

def delIntegrante(request, id):
    supabase.table("integrantes").delete().eq("id", id).execute()
    return redirect('integrantes')

@api_view(['GET', 'POST'])
def categorias_api(request):
    if request.method=='GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
def categoria_api(request, id):
    categoria = Categoria.objects.get(id=id)
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    elif request.method=='GET':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def relatorios(request):
    servicos = Servico.objects.all()
    servicos_ativos = servicos.filter(ativo=True).count()
    servicos_inativos = servicos.filter(ativo=False).count()

    categorias = servicos.values('categoria__nome').annotate(quantidade=Count('id'))

    return render(request, 'relatorios.html', {
        'servicos_ativos': servicos_ativos,
        'servicos_inativos': servicos_inativos,
        'status_valores': [servicos_ativos, servicos_inativos],
        'categorias_labels': [
            item['categoria__nome'] or 'Sem categoria'
            for item in categorias
        ],
        'categorias_valores': [
            item['quantidade']
            for item in categorias
        ],
    })