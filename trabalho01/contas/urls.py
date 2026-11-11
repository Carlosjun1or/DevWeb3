from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='contas_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_contas'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout_contas'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/', views.perfil, name='perfil_contas'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='alterar_senha.html', success_url=reverse_lazy('perfil_contas')), name='alterar_senha'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='alterar_senha.html', success_url=reverse_lazy('perfil_contas')), name='alterar_senha_contas'),
    path('cadastro/', views.cadastro, name='cadastrar_usuario'),
    path('cadastro/', views.cadastro, name='cadastro_contas'),
    path('cadastrar/', views.cadastro, name='cadastrar_usuario_contas'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='registration/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
