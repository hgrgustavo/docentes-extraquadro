from django.contrib.auth import hashers
from django.db import models
from django.core import validators, exceptions
import os


class Professor(models.Model):
    CHOICES = [
        ("PF", "Pessoa Física"),
        ("PJ", "Pessoa Jurídica"),
    ]

    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observacao = models.TextField()
    pf_ou_pj = models.CharField(max_length=15, choices=CHOICES)
    cpf = models.CharField(max_length=14, null=True, blank=True, validators=[validators.RegexValidator(
        regex=r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}$')])
    cnpj = models.CharField(max_length=18, null=True, blank=True, validators=[
                            validators.RegexValidator(regex=r'^\d{2}\.?(\d{3}\.?){2}/?\d{4}-?\d{2}$')])

    class Meta:
        db_table = 'professor'

    def clean(self):
        if self.pf_ou_pj == "PF" and self.cnpj:
            raise exceptions.ValidationError("Pessoa Física não pode ter CNPJ")

        if self.pf_ou_pj == "PJ" and self.cpf:
            raise exceptions.ValidationError(
                "Pessoa Jurídica não pode ter CPF")


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=255, validators=[
        validators.EmailValidator])
    numero_telefone = models.CharField(max_length=45, validators=[
        validators.RegexValidator(regex=r'^\+?\d{10,15}$')])
    senha = models.CharField(max_length=512, default="")

    def save(self, *args, **kwargs):
        if self.senha:
            self.senha = hashers.make_password(
                self.senha,
                salt=os.urandom(16).hex(),
                hasher=hashers.ScryptPasswordHasher()
            )
        super().save(*args, **kwargs)

    def check_password(self, password):
        return hashers.check_password(password, self.senha)

    class Meta:
        db_table = 'usuario'


class Contratos(models.Model):
    CHOICES_MODALIDADES = [
        ("hora-aula", "Hora-aula"),
    ]

    processo = models.CharField(max_length=255)
    evento = models.DateField()
    prestador = models.CharField(max_length=255)
    servico = models.CharField(max_length=255)
    componentes = models.CharField(max_length=255)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField()
    valor_hora_aula = models.FloatField()
    modalidade = models.CharField(
        max_length=50, default="hora-aula", choices=CHOICES_MODALIDADES)

    class Meta:
        db_table = 'contratos'

    def get_pdf_context(self):
        return {
            "id": self.pk,
            "processo": self.processo,
            "evento": self.evento,
            "prestador": self.prestador,
            "servico": self.servico,
            "componentes": self.componentes,
            "data_inicio": self.data_inicio,
            "data_termino": self.data_termino,
            "carga_horaria": self.carga_horaria,
            "valor_hora_aula": self.valor_hora_aula,
            "total_valor": self.valor_hora_aula * self.carga_horaria,
        }
