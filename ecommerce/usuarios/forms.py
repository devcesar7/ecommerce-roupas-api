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
        widgets = {
            'tipo': forms.RadioSelect(choices=Usuario.TIPO_PESSOA),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefone'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail pessoal'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Data de nascimento'
            }),
            'preferencia': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
