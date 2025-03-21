
from django.db import models


class ControlePagamento(models.Model):
    situacao_pasta = models.CharField(max_length=45)
    solicitacao = models.ForeignKey('Solicitacao', models.DO_NOTHING, default="")
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
    observacao = models.TextField()
    professor = models.ForeignKey('Professor', models.DO_NOTHING, default="")

    class Meta:
        
        db_table = 'controle_pagamento'
        unique_together = (('id', 'solicitacao', 'professor'),)


class Professor(models.Model):
    choices = {
        "PF": "Pessoa Física", 
        "PJ": "Pessoa Jurídica",
    }
    
    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observacao = models.CharField(max_length=45)
    pf_ou_pj = models.CharField(max_length=15, choices=choices)

    class Meta:
        
        db_table = 'professor'


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
    prestador = models.CharField(max_length=45)
    curso_treinamento = models.CharField(max_length=45)
    servico = models.TextField()
    observacao = models.TextField()

    class Meta:
        
        db_table = 'solicitacao'


class Usuario(models.Model):
    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    numero_telefone = models.CharField(max_length=45)
    senha = models.CharField(max_length=45, default="")

    class Meta:
        
        db_table = 'usuario'
