from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import LoginForm


urlpatterns= [
    path("", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", auth_views.PasswordChangeView.as_view(template_name="alterar_senha.html", success_url=reverse_lazy("perfil")), name="alterar_senha"),
    path("cadastro/", views.cadastro, name="cadastrar_usuario"),
]