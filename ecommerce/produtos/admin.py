from django.contrib import admin
from .models import Categoria, Subcategoria, Produto

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Produto)