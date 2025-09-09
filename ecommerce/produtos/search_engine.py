import spacy
from django.db.models import Q
from .models import Produto, Categoria, Subcategoria, Marca
import unicodedata

# Função para remover acentos e caracteres especiais
def remove_acento(texto):
    if not isinstance(texto, str):
        return texto
    texto_sem_acento = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto_sem_acento

try:
    nlp = spacy.load("pt_core_news_sm")
except ImportError:
    print("Modelo do spaCy não encontrado. Execute 'python -m spacy download pt_core_news_sm'")
    nlp = None

SINONIMOS_MAP = {
    # ... (o seu dicionário de sinônimos permanece o mesmo)
    "camisa": ["camisas", "blusa", "blusas", "camiseta", "camisetas", "camisa polo", "camisas polo", "top", "tops", "regata", "regatas", "bata", "batas", "corpete", "corpetes", "blusinha", "blusinhas", "camisete", "camisetes"],
    "blusa": ["blusas", "camisa", "camisas", "camiseta", "camisetas", "regata", "regatas", "blusinha", "blusinhas"],
    "camiseta": ["camisetas", "t-shirt", "t-shirts", "camisa", "camisas", "blusa", "blusas", "top", "tops"],
    "cropped": ["croppeds", "blusa cropped", "camisa cropped", "top cropped"],
    "calça": ["calças", "jeans", "calça jeans", "jeans skinny", "calça skinny", "calça reta", "calça pantalona", "pantalonas", "legging", "leggings", "calça de moletom", "calças de moletom", "bermuda", "bermudas", "shorts", "calção", "calções", "jogger", "joggers"],
    "jeans": ["calça jeans", "calças jeans", "denim"],
    "casaco": ["casacos", "jaqueta", "jaquetas", "jaqueta jeans", "jaqueta de couro", "moletom", "moletons", "agasalho", "agasalhos", "blazer", "blazers", "cardigã", "cardigãs", "parka", "parkas"],
    "moletom": ["moletons", "casaco de moletom", "blusão", "blusões", "hoodie", "hoodies"],
    "vestido": ["vestidos", "vestidinho", "vestidinhos", "maxi vestido", "vestido de festa", "vestido casual"],
    "saia": ["saias", "saia jeans", "saia longa", "saia curta", "minissaia"],
    "sapato": ["sapatos", "tênis", "tênis", "sapatilha", "sapatilhas", "sandália", "sandálias", "chinelo", "chinelos", "bota", "botas", "salto", "saltos", "sapato social", "sapato casual"],
    "tênis": ["tênis", "sapato", "sapatos", "calçado esportivo", "sneaker", "sneakers"],
    "bolsa": ["bolsas", "mochila", "mochilas", "carteira", "carteiras"],
    "cinto": ["cintos"],
    "óculos": ["oculos", "óculos de sol"],
    "chapéu": ["chapéus", "boné", "bonés"],
    "colar": ["colares", "cordão", "gargantilha"],
    "anel": ["anéis"],
    "brinco": ["brincos"],
    "biquíni": ["biquinis", "biquini", "maiô", "maiôs"],
    "sunga": ["sungas"],
    "cueca": ["cuecas"],
    "calcinha": ["calcinhas"],
    "sutiã": ["sutiãs"],
    "roupa": ["roupas", "vestuário", "traje", "trajes", "peça de roupa"],
    "moda": ["estilo", "tendência"],
    "feminino": ["feminina", "mulher", "mulheres", "menina", "meninas"],
    "masculino": ["masculina", "homem", "homens", "menino", "meninos"],
    "infantil": ["infantis", "criança", "crianças", "menino", "menina"],
    "acessório": ["acessórios", "complemento", "complementos"],
}

def get_related_terms(query):
    # ... (o código desta função permanece o mesmo)
    if not nlp or not query:
        return [query]
    query_lower = query.lower()
    query_doc = nlp(query_lower)
    termos_busca = set()
    for token in query_doc:
        termos_busca.add(token.text)
        termos_busca.add(token.lemma_)
        termos_busca.add(remove_acento(token.text))
        termos_busca.add(remove_acento(token.lemma_))
    termos_expandidos = set(termos_busca)
    for termo in termos_busca:
        for palavra_chave, sinonimos in SINONIMOS_MAP.items():
            if termo in [s.lower() for s in sinonimos]:
                termos_expandidos.add(palavra_chave.lower())
                termos_expandidos.update([s.lower() for s in sinonimos])
            if termo in [remove_acento(s.lower()) for s in sinonimos]:
                termos_expandidos.add(palavra_chave.lower())
                termos_expandidos.update([s.lower() for s in sinonimos])
    return list(termos_expandidos)


def perform_product_search(request_get):
    """
    Executa a busca de produtos aplicando todos os filtros da URL de forma cumulativa.
    Recebe o QueryDict (request.GET) como parâmetro.
    """
    produtos = Produto.objects.all()
    q = ''

    query = request_get.get('q')
    if query:
        q = query
        termos_busca = get_related_terms(query)
        query_set = Q()
        for termo in termos_busca:
            query_set |= (
                Q(nome__icontains=termo) |
                Q(descricao__icontains=termo) |
                Q(categoria__nome__icontains=termo) |
                Q(subcategoria__nome__icontains=termo) |
                Q(marca__nome__icontains=termo)
            )
        produtos = produtos.filter(query_set).distinct()
    
    # --- Aplicação dos filtros da barra lateral de forma cumulativa ---
    
    genero_filtro = request_get.get('genero')
    if genero_filtro:
        produtos = produtos.filter(genero__iexact=genero_filtro)

    categoria_filtro = request_get.get('categoria')
    if categoria_filtro:
        produtos = produtos.filter(categoria__nome__iexact=categoria_filtro)
    
    # CORREÇÃO: Pegue uma lista de tamanhos e filtre usando o lookup '__in'
    tamanho_filtro = request_get.getlist('tamanho')
    if tamanho_filtro:
        produtos = produtos.filter(tamanhos__nome__in=tamanho_filtro).distinct()

    marca_filtro = request_get.get('marca')
    if marca_filtro:
        produtos = produtos.filter(marca__nome__iexact=marca_filtro)
    
    preco_filtro = request_get.get('preco')
    if preco_filtro:
        faixa = preco_filtro.split('-')
        if len(faixa) == 2:
            preco_min = float(faixa[0])
            preco_max = float(faixa[1])
            produtos = produtos.filter(preco__gte=preco_min, preco__lte=preco_max)
        elif len(faixa) == 1 and faixa[0]:
            preco_min = float(faixa[0])
            produtos = produtos.filter(preco__gte=preco_min)

    # Ordenação dos produtos
    sort_by = request_get.get('sort-by', 'mais_populares')
    if sort_by == 'menor_preco':
        produtos = produtos.order_by('preco')
    elif sort_by == 'maior_preco':
        produtos = produtos.order_by('-preco')
    else:
        produtos = produtos.order_by('-criado_em')

    return produtos, q