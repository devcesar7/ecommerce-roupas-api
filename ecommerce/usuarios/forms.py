from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CadastroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'tipo',
            'first_name',
            'last_name',
            'cpf',
            'telefone',
            'endereco',
            'email',
            'data_nascimento',
            'preferencia',
            'password1',
            'password2',
        ]
