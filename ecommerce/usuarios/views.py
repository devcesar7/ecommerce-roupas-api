from django.shortcuts import render, redirect
from .forms import CadastroForm
from django.contrib.auth import login

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home_public')  # ou outra página
    else:
        form = CadastroForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def login_view(request):
    return render(request, 'usuarios/login.html')

