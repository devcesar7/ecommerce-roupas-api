from produtos.models import Marca

marcas = ['Sem marca','Nike','Adidas','Puma','Hering','Levis','Zara','Reserva']
for m in marcas:
    Marca.objects.get_or_create(nome=m)
print('Marcas criadas/confirmadas')
