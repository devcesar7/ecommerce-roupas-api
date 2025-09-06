from django.db import migrations


def create_marcas(apps, schema_editor):
    Marca = apps.get_model('produtos', 'Marca')
    marcas = ['Sem marca', 'Nike', 'Adidas', 'Puma', 'Hering', 'Levis', 'Zara', 'Reserva']
    for nome in marcas:
        Marca.objects.get_or_create(nome=nome)


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_estoquetamanho'),
    ]

    operations = [
        migrations.RunPython(create_marcas, reverse_code=migrations.RunPython.noop),
    ]
