from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

def logout_view(request):
    logout(request)
    return redirect('home_public')
from django.contrib import messages
from .forms import CadastroForm, EmailAuthenticationForm


def cadastro_view(request):
    """Cadastro de novo usuário"""
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # login automático
            messages.success(request, "Cadastro realizado com sucesso! 🚀")
            return redirect('home_public')
        else:
            messages.error(request, "Erro no formulário. Verifique os campos e tente novamente.")
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


def login_view(request):
    """Login de usuário já cadastrado"""
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Se o usuário não marcou "Manter-me logado", a sessão expira ao fechar o navegador
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # expira ao fechar o navegador
            else:
                request.session.set_expiry(1209600)  # 2 semanas
            messages.success(request, f"Bem-vindo de volta, {user.first_name}! 🎉")
            return redirect('home_public')
        else:
            messages.error(request, "E-mail ou senha inválidos. Verifique e tente novamente.")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})
