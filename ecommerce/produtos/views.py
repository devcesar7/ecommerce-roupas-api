from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProdutoForm

@login_required
def cadastrar_produto(request):
    if not request.user.is_superuser:
        return redirect('home') 

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.dono = request.user
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar.html', {'form': form})