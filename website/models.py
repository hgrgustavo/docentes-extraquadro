from django.contrib.auth import hashers
from django.db import models
from django.core import validators, exceptions
import os


class ControlePagamento(models.Model):
    situacao_pasta = models.CharField(max_length=45)
    solicitacao = models.ForeignKey(
        'Solicitacao', models.DO_NOTHING, default="")
    data_inicio = models.DateField()
    data_termino = models.DateField()
    modalidade = models.CharField(max_length=45, default="hora-aula")
    curso_componentes = models.CharField(max_length=45)
    evento = models.CharField(max_length=45)
    solicitante = models.CharField(max_length=45)
    fornecedor = models.CharField(max_length=45)
    valor_sc = models.FloatField()
    total_horas_contradas = models.IntegerField()
    valor_hora_aula = models.FloatField()
    valor_pago = models.FloatField()
    saldo = models.FloatField()
    saldo_de_horas = models.IntegerField()
    horas_pagas = models.IntegerField()
    prazo_validade_contrato = models.DateField()
    observacao = models.TextField()
    professor = models.ForeignKey('Professor', models.DO_NOTHING, default="")

    class Meta:

        db_table = 'controle_pagamento'
        unique_together = (('id', 'solicitacao', 'professor'),)


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
        regex=r'([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})')])
    cnpj = models.CharField(max_length=18, null=True, blank=True, validators=[
                            validators.RegexValidator(regex=r'/^[0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2}$/')])

    class Meta:
        db_table = 'professor'

    def clean(self):
        if self.pf_ou_pj == "PF" and self.cnpj:
            raise exceptions.ValidationError("Pessoa Física não pode ter CNPJ")

        if self.pf_ou_pj == "PJ" and self.cpf:
            raise exceptions.ValidationError(
                "Pessoa Jurídica não pode ter CPF")

    # implementar mascaras p/ cpf e cnpj


class Solicitacao(models.Model):
    status = models.CharField(max_length=45)
    parecer_coordenacao = models.TextField()
    parecer_secretaria = models.TextField()
    parecer_compras = models.TextField()
    pendencias = models.TextField()
    evento_sige = models.CharField(max_length=45)
    processo = models.CharField(max_length=45)
    solicitante = models.CharField(max_length=45)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    horario_inicio = models.TimeField()
    horario_termino = models.TimeField()
    carga_horaria = models.IntegerField()
    valor_hora = models.FloatField()
    prestador = models.CharField(max_length=255)
    curso_treinamento = models.TextField()
    servico = models.TextField()
    observacao = models.TextField()

    class Meta:
        db_table = 'solicitacao'


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
    processo = models.CharField(max_length=255)
    evento = models.DateField()
    prestador = models.CharField(max_length=255)
    servico = models.CharField(max_length=255)
    componentes = models.CharField(max_length=255)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    carga_horaria = models.IntegerField()
    valor_hora_aula = models.FloatField()
    pdf = models.FileField(
        upload_to="contratos/hora-aula/", null=True, blank=True)
