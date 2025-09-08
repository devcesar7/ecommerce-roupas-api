from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import ProdutoForm
from .models import Produto, Categoria
from .search_engine import perform_product_search

# IMPORTAÇÃO QUE VOCÊ DEVE ADICIONAR
from django.core.paginator import Paginator


@login_required
def cadastrar_produto(request):
    # ... (o código desta função permanece o mesmo)
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar.html', {'form': form})


def pesquisa_produtos(request):
    q = request.GET.get('q') or request.GET.get('busca')
    categoria_param = request.GET.get('categoria')

    # A sua função 'perform_product_search' retorna a lista completa de produtos.
    # A paginação será aplicada a essa lista.
    produtos_list = perform_product_search(request.GET)

    categorias = Categoria.objects.all()

    # Configura a paginação
    paginator = Paginator(produtos_list, 12)  # Mostra 12 produtos por página
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)

    context = {
        'produtos': produtos,
        'q': q,
        'categoria': categoria_param,
        'categorias': categorias,
    }
    return render(request, 'produtos/busca.html', context)