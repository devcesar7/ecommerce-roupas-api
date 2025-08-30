from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CadastroForm


def cadastro_view(request):
    """Cadastro de novo usuário"""
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Faz login automático após cadastro
            messages.success(request, "Cadastro realizado com sucesso! Bem-vindo à Ganyk Store 🚀")
            return redirect('home_public')  # ajuste a rota conforme seu sistema
        else:
            messages.error(request, "Houve um erro no formulário. Verifique os campos e tente novamente.")
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


def login_view(request):
    """Login de usuário já cadastrado"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo de volta, {user.username}! 🎉")
            return redirect('home_public')
        else:
            messages.error(request, "Usuário ou senha inválidos. Verifique e tente novamente.")
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})
