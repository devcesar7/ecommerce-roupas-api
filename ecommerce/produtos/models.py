from django.db import models
from django.conf import settings  # Importa o modelo de usuário customizado

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            # Remove espaços extras e formata cada palavra com inicial maiúscula
            self.nome = self.nome.strip().title()
        super().save(*args, **kwargs)

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.categoria.nome} - {self.nome}"

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.strip().title()
        super().save(*args, **kwargs)

class Produto(models.Model):
    # dono removido: apenas admins podem criar produtos via admin
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
    # Relacionamento com tamanhos: ManyToMany para permitir múltiplos tamanhos por produto
    # O modelo Tamanho é definido abaixo
    tamanhos = models.ManyToManyField('Tamanho', blank=True)
    # Marca do produto
    marca = models.ForeignKey('Marca', on_delete=models.SET_NULL, null=True, blank=True)
    imagem_principal = models.ImageField(upload_to='produtos/')
    imagem_secundaria = models.ImageField(upload_to='produtos/', blank=True, null=True)
    imagem_detalhe = models.ImageField(upload_to='produtos/', blank=True, null=True)
    estoque = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            # Formata o nome do produto para Title Case antes de salvar
            self.nome = self.nome.strip().title()
        super().save(*args, **kwargs)


class Marca(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.strip().title()
        super().save(*args, **kwargs)


class Tamanho(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.strip().upper()
        super().save(*args, **kwargs)


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/')
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.produto.nome} - imagem {self.ordem}"


class EstoqueTamanho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='estoque_tamanhos')
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('produto', 'tamanho')

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho.nome}: {self.quantidade}"
