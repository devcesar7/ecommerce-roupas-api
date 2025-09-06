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
    # O modelo 'pt_core_news_sm' já inclui lematização
    nlp = spacy.load("pt_core_news_sm")
except ImportError:
    print("Modelo do spaCy não encontrado. Execute 'python -m spacy download pt_core_news_sm'")
    nlp = None

SINONIMOS_MAP = {
    # Camisas e tops
    "camisa": ["camisas", "blusa", "blusas", "camiseta", "camisetas", "camisa polo", "camisas polo", "top", "tops", "regata", "regatas", "bata", "batas", "corpete", "corpetes", "blusinha", "blusinhas", "camisete", "camisetes"],
    "blusa": ["blusas", "camisa", "camisas", "camiseta", "camisetas", "regata", "regatas", "blusinha", "blusinhas"],
    "camiseta": ["camisetas", "t-shirt", "t-shirts", "camisa", "camisas", "blusa", "blusas", "top", "tops"],
    "cropped": ["croppeds", "blusa cropped", "camisa cropped", "top cropped"],
    
    # Calças
    "calça": ["calças", "jeans", "calça jeans", "jeans skinny", "calça skinny", "calça reta", "calça pantalona", "pantalonas", "legging", "leggings", "calça de moletom", "calças de moletom", "bermuda", "bermudas", "shorts", "calção", "calções", "jogger", "joggers"],
    "jeans": ["calça jeans", "calças jeans", "denim"],

    # Roupas de frio e agasalhos
    "casaco": ["casacos", "jaqueta", "jaquetas", "jaqueta jeans", "jaqueta de couro", "moletom", "moletons", "agasalho", "agasalhos", "blazer", "blazers", "cardigã", "cardigãs", "parka", "parkas"],
    "moletom": ["moletons", "casaco de moletom", "blusão", "blusões", "hoodie", "hoodies"],

    # Vestidos e saias
    "vestido": ["vestidos", "vestidinho", "vestidinhos", "maxi vestido", "vestido de festa", "vestido casual"],
    "saia": ["saias", "saia jeans", "saia longa", "saia curta", "minissaia"],

    # Calçados
    "sapato": ["sapatos", "tênis", "tênis", "sapatilha", "sapatilhas", "sandália", "sandálias", "chinelo", "chinelos", "bota", "botas", "salto", "saltos", "sapato social", "sapato casual"],
    "tênis": ["tênis", "sapato", "sapatos", "calçado esportivo", "sneaker", "sneakers"],

    # Acessórios
    "bolsa": ["bolsas", "mochila", "mochilas", "carteira", "carteiras"],
    "cinto": ["cintos"],
    "óculos": ["oculos", "óculos de sol"],
    "chapéu": ["chapéus", "boné", "bonés"],
    "colar": ["colares", "cordão", "gargantilha"],
    "anel": ["anéis"],
    "brinco": ["brincos"],
    
    # Roupas de banho
    "biquíni": ["biquinis", "biquini", "maiô", "maiôs"],
    "sunga": ["sungas"],

    # Roupas íntimas
    "cueca": ["cuecas"],
    "calcinha": ["calcinhas"],
    "sutiã": ["sutiãs"],

    # Termos genéricos para abranger mais buscas
    "roupa": ["roupas", "vestuário", "traje", "trajes", "peça de roupa"],
    "moda": ["estilo", "tendência"],
    "feminino": ["feminina", "mulher", "mulheres", "menina", "meninas"],
    "masculino": ["masculina", "homem", "homens", "menino", "meninos"],
    "infantil": ["infantis", "criança", "crianças", "menino", "menina"],
    "acessório": ["acessórios", "complemento", "complementos"],

}

def get_related_terms(query):
    """
    Usa a lematização e a remoção de acentos para encontrar termos relacionados.
    """
    if not nlp or not query:
        return [query]

    query_lower = query.lower()
    query_doc = nlp(query_lower)

    termos_busca = set()
    
    # 1. Processa cada "token" (palavra) da busca do usuário
    for token in query_doc:
        # Adiciona o termo original, o termo lematizado (singular) e a versão sem acento
        termos_busca.add(token.text)
        termos_busca.add(token.lemma_)
        termos_busca.add(remove_acento(token.text))
        termos_busca.add(remove_acento(token.lemma_))
    
    # 2. Expande a busca com o dicionário de sinônimos
    termos_expandidos = set(termos_busca)
    for termo in termos_busca:
        for palavra_chave, sinonimos in SINONIMOS_MAP.items():
            if termo in [s.lower() for s in sinonimos]:
                termos_expandidos.add(palavra_chave.lower())
                termos_expandidos.update([s.lower() for s in sinonimos])
            # Adiciona a versão sem acento do dicionário
            if termo in [remove_acento(s.lower()) for s in sinonimos]:
                termos_expandidos.add(palavra_chave.lower())
                termos_expandidos.update([s.lower() for s in sinonimos])
    
    return list(termos_expandidos)


def perform_product_search(request_params):
    """
    Executa a busca de produtos com a lógica de lematização e acentos.
    """
    q = request_params.get('q') or request_params.get('busca')
    categoria = request_params.get('categoria')

    produtos = Produto.objects.all().order_by('-criado_em')
    
    if q:
        termos_busca = get_related_terms(q)
        
        query_set = Q()
        for termo in termos_busca:
            # __icontains já cuida da capitalização
            query_set |= (
                Q(nome__icontains=termo) |
                Q(descricao__icontains=termo) |
                Q(categoria__nome__icontains=termo) |
                Q(subcategoria__nome__icontains=termo) |
                Q(marca__nome__icontains=termo)
            )
        produtos = produtos.filter(query_set).distinct()

    if categoria:
        # Busca por categoria com e sem acento
        categoria_original = categoria
        categoria_sem_acento = remove_acento(categoria)
        
        produtos = produtos.filter(
            Q(genero__iexact=categoria_original) | Q(categoria__nome__iexact=categoria_original) |
            Q(genero__iexact=categoria_sem_acento) | Q(categoria__nome__iexact=categoria_sem_acento)
        )

    return produtos