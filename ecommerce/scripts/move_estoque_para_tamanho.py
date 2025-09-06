# Script para migrar valores do campo `estoque` (Produto) para registros `EstoqueTamanho` usando um tamanho padrão 'Único'.
# Uso: executar após aplicar migrations: python manage.py shell < scripts/move_estoque_para_tamanho.py

from produtos.models import Produto, Tamanho, EstoqueTamanho

# Garante que exista um tamanho padrão
padrao, created = Tamanho.objects.get_or_create(nome='ÚNICO')

count = 0
for p in Produto.objects.all():
    try:
        quantidade = int(getattr(p, 'estoque', 0) or 0)
    except Exception:
        quantidade = 0
    if quantidade > 0:
        eto, created = EstoqueTamanho.objects.get_or_create(produto=p, tamanho=padrao, defaults={'quantidade': quantidade})
        if not created:
            eto.quantidade = quantidade
            eto.save()
        count += 1

print(f'Processados {count} produtos: valores migrados para EstoqueTamanho ({padrao.nome}).')
