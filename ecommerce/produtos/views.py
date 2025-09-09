from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ProdutoForm
from .models import Produto, Categoria, Marca, ProdutoImagem, EstoqueTamanho
from .search_engine import perform_product_search


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
    produtos_list, q = perform_product_search(request.GET)
    paginator = Paginator(produtos_list, 12)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    
    # NOVO: captura o filtro de categoria para a página
    filtro_categoria_ativo = request.GET.get('categoria')

    context = {
        'produtos': produtos,
        'q': q,
        'categorias': categorias,
        'marcas': marcas,
        'filtro_categoria_ativo': filtro_categoria_ativo,
    }
    return render(request, 'produtos/busca.html', context)


# NOVA FUNÇÃO DE VISUALIZAÇÃO
def produto_detalhe(request, pk):
    # Obtém o produto ou retorna 404 se não existir
    produto = get_object_or_404(Produto, pk=pk) # <-- Adicione 'produto = ' aqui
    
    # Obtém todas as imagens do produto
    imagens = ProdutoImagem.objects.filter(produto=produto).order_by('ordem')
    
    # Obtém o estoque por tamanho
    estoque_por_tamanho = EstoqueTamanho.objects.filter(produto=produto)
    
    # Cria um dicionário para fácil acesso no template
    tamanhos_com_estoque = {}
    for et in estoque_por_tamanho:
        tamanhos_com_estoque[et.tamanho.nome] = et.quantidade > 0
    
    context = {
        'produto': produto,
        'imagens': imagens,
        'tamanhos_com_estoque': tamanhos_com_estoque,
        'tamanhos_disponiveis': estoque_por_tamanho,
    }
    
    return render(request, 'produtos/produto_detalhe.html', context)