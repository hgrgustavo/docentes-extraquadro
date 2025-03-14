# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ControlePagamento(models.Model):
    situaþÒo_pasta = models.CharField(max_length=45)
    solicitaþÒo = models.ForeignKey('Solicitao', models.DO_NOTHING)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    modalidade = models.CharField(max_length=45)
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
    observaþÒo = models.TextField()
    professor = models.ForeignKey('Professor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'controle_pagamento'
        unique_together = (('id', 'solicitaþÒo', 'professor'),)


class Professor(models.Model):
    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observaþÒo = models.CharField(max_length=45)
    pf_ou_pj = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'professor'


class Solicitao(models.Model):
    status = models.CharField(max_length=45)
    parecer_coordenaþÒo = models.TextField()
    parecer_secretaria = models.TextField()
    parecer_compras = models.TextField()
    pendÛncias = models.TextField()
    evento_sige = models.CharField(max_length=45)
    processo = models.CharField(max_length=45)
    solicitante = models.CharField(max_length=45)
    data_inicio = models.DateField()
    data_tÚrmino = models.DateField()
    horßrio_inicio = models.TimeField()
    horßrio_tÚrmino = models.TimeField()
    carga_horaria = models.IntegerField()
    valor_hora = models.FloatField()
    prestador = models.CharField(max_length=45)
    curso_treinamento = models.CharField(max_length=45)
    serviþo = models.TextField()
    observaþÒo = models.TextField()

    class Meta:
        managed = False
        db_table = 'solicitaþÒo'


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    n·mero_telefone = models.CharField(max_length=45)
    senha = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'usuario'
