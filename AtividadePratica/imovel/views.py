from django.shortcuts import redirect, render
from .models import Imovel, Corretor
from .forms import FormImovel, FormCorretor 

# Create your views here.

def index(request):
    return redirect("imoveis")

def add_imovel(request):
    form = FormImovel(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('imoveis')
        
    return render(request, "cadastro-imovel.html", {"form": form})

def edit_imovel(request, id):
    imovel = Imovel.objects.get(id=id)
    form = FormImovel(request.POST or None, request.FILES or None, instance=imovel)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('imoveis')
        
    return render(request, "cadastro-imovel.html", {'form': form})

def del_imovel(request, id):
    imovel = Imovel.objects.get(id=id)
    imovel.imagem.delete(save=False)
    imovel.delete()
    return redirect('imoveis')

def add_corretor(request):
    form = FormCorretor(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('corretores')
        
    return render(request, "cadastro-corretor.html", {"form": form})

def edit_corretor(request, id):
    corretor = Corretor.objects.get(id=id)
    form = FormCorretor(request.POST or None, instance=corretor)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('corretores')
        
    return render(request, "cadastro-corretor.html", {'form': form})

def del_corretor(request, id):
    corretor = Corretor.objects.get(id=id)
    corretor.delete()
    return redirect('corretores')

def imoveis(request):
    imoveis = Imovel.objects.all()
    busca = request.GET.get("busca", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    finalidade = request.GET.get("finalidade", "").strip()
    cidade = request.GET.get("cidade", "").strip()
    preco_maximo = request.GET.get("preco_maximo", "").strip()
    quartos = request.GET.get("quartos", "").strip()

    if busca:
        imoveis = imoveis.filter(titulo__icontains=busca)
    if tipo:
        imoveis = imoveis.filter(tipo=tipo)
    if finalidade:
        imoveis = imoveis.filter(finalidade__icontains=finalidade)
    if cidade:
        imoveis = imoveis.filter(cidade__icontains=cidade)
    if preco_maximo:
        imoveis = imoveis.filter(preco__lte=preco_maximo)
    if quartos:
        imoveis = imoveis.filter(quantidade_quartos=quartos)

    filtros_ativos = any(
        (busca, tipo, finalidade, cidade, preco_maximo, quartos)
    )

    return render(
        request,
        "imovel.html",
        {"imoveis": imoveis, "filtros_ativos": filtros_ativos},
    )

def corretores(request):
    corretores = Corretor.objects.all()
    busca = request.GET.get("busca", "").strip()

    if busca:
        corretores = corretores.filter(
            nome__icontains=busca
        ) | Corretor.objects.filter(
            email__icontains=busca
        ) | Corretor.objects.filter(
            telefone__icontains=busca
        )
        corretores = corretores.distinct()

    return render(
        request,
        "corretor.html",
        {"corretores": corretores, "busca": busca},
    )
