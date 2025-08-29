from django.urls import path
from .views import cadastro_view, login_view

urlpatterns = [
    path('cadastro/', cadastro_view, name='cadastro'),
    path('login/', login_view, name='login'),
]
