from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
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
   

    return render(request, "perfil.html")