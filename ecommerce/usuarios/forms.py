from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from datetime import date

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
            'tipo': forms.RadioSelect(choices=Usuario.TIPO_PESSOA, attrs={'class': 'tipo-pessoa'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail pessoal'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Ano de nascimento'}),
            'preferencia': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha sua preferência de moda'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})
        # Adiciona uma opção inicial personalizada ao select de preferência
        self.fields['preferencia'].empty_label = 'Escolha sua preferência de moda'
        # Impede seleção de datas futuras no campo de data de nascimento (cliente)
        if 'data_nascimento' in self.fields:
            try:
                self.fields['data_nascimento'].widget.attrs.update({'max': date.today().isoformat()})
            except Exception:
                pass

    def clean_data_nascimento(self):
        data = self.cleaned_data.get('data_nascimento')
        if data and data > date.today():
            raise forms.ValidationError('A data de nascimento não pode ser no futuro.')
        return data


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'})
    )
    remember_me = forms.BooleanField(
        label="Manter-me logado",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
