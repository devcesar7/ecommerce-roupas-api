from django.urls import path
from . import views

urlpatterns = [
    path('produtos/pesquisa/', views.pesquisa_produtos, name='pesquisa_produtos'),
]