from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"

class Produto(models.Model):
    dono = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True)
    genero = models.CharField(max_length=20, choices=[
        ('Feminino', 'Feminino'),
        ('Masculino', 'Masculino'),
        ('Infantil', 'Infantil'),
        ('Unissex', 'Unissex'),
    ])
    tamanho = models.CharField(max_length=10, choices=[
        ('PP', 'PP'), ('P', 'P'), ('M', 'M'), ('G', 'G'), ('GG', 'GG'),
        ('36', '36'), ('38', '38'), ('40', '40'), ('42', '42'), ('44', '44'),
    ])
    imagem_principal = models.ImageField(upload_to='produtos/')
    imagem_secundaria = models.ImageField(upload_to='produtos/', blank=True, null=True)
    imagem_detalhe = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.nome