from django.contrib import admin
from .models import Categoria, Subcategoria, Produto, Marca, Tamanho, ProdutoImagem, EstoqueTamanho


class ProdutoImagemInline(admin.TabularInline):
	model = ProdutoImagem
	extra = 1


class EstoqueTamanhoInline(admin.TabularInline):
	model = EstoqueTamanho
	extra = 1
	verbose_name = 'Estoque por Tamanho'
	verbose_name_plural = 'Estoque por Tamanho'


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'categoria', 'marca', 'preco', 'ativo')
	list_filter = ('categoria', 'marca', 'genero', 'ativo')
	inlines = [ProdutoImagemInline, EstoqueTamanhoInline]

	def has_add_permission(self, request):
		# somente superusers podem adicionar produtos via admin
		return request.user.is_superuser


admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Marca)
admin.site.register(Tamanho)