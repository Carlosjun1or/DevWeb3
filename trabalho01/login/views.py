from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CadastroForm
from .models import Perfil


@login_required
def dashboard(request):
    perfil = Perfil.objects.get(usuario=request.user)
    
    if perfil.tipo_usuario == 'administrador':
        return render(request, "/admin/")
    else:
      return render(request, "dashboard.html")

@login_required
def perfil(request):
    if request.method == "POST":
        # Aqui você pode adicionar a lógica para atualizar o perfil do usuário
        usuario = request.user
        usuario.first_name = request.POST.get("first_name", usuario.first_name)
        usuario.last_name = request.POST.get("last_name", usuario.last_name)
        usuario.email = request.POST.get("email", usuario.email)
        usuario.save()
        
        return render(request, "perfil.html", {"mensagem": "Perfil atualizado com sucesso!"})
   
    return render(request, "perfil.html", {"usuario": request.user})

def cadastro(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()
                Perfil.objects.create(usuario=usuario, tipo_usuario='cliente')  # Define o tipo de usuário como 'cliente' por padrão
            messages.success(request, "Usuário cadastrado com sucesso! Você já pode entrar.")
            return redirect("login")
    else:
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})