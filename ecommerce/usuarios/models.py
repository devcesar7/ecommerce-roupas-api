from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo Email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    username = None  # removemos o username padrão
    email = models.EmailField(unique=True)

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "cpf"]

    objects = UsuarioManager()

    def __str__(self):
        return self.email
