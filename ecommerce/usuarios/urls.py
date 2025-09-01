from django.urls import path
from .views import cadastro_view, login_view, logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', cadastro_view, name='cadastro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html',
        email_template_name='usuarios/password_reset_email.html',
        subject_template_name='usuarios/password_reset_subject.txt',
        success_url='/usuarios/recuperar-senha-feito/'
    ), name='password_reset'),
    path('recuperar-senha-feito/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html',
        success_url='/usuarios/reset-completo/'
    ), name='password_reset_confirm'),
    path('reset-completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'), name='password_reset_complete'),
]
