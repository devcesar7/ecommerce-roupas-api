from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_PESSOA = [
        ('F', 'Pessoa Física'),
        ('J', 'Pessoa Jurídica'),
    ]

    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    preferencia = models.CharField(max_length=20, choices=[
        ('feminina', 'Moda Feminina'),
        ('masculina', 'Moda Masculina'),
    ], blank=True)
    tipo = models.CharField(max_length=1, choices=TIPO_PESSOA, default='F')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
