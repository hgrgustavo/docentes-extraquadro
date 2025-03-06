from django.db import models


class ControlePagamento(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, solicitação_id, professor_id) found, that is not supported. The first column is selected.
    situação_pasta = models.CharField(max_length=45)
    solicitação = models.ForeignKey('Solicitao', models.DO_NOTHING, unique=True)
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
    observação = models.TextField()
    professor = models.ForeignKey('Professor', models.DO_NOTHING)

    class Meta:
        
        db_table = 'controle_pagamento'
        unique_together = (('id', 'solicitação', 'professor'),)


class Login(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, usuario_id) found, that is not supported. The first column is selected.
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)

    class Meta:
        
        db_table = 'login'
        unique_together = (('id', 'usuario'),)


class Professor(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    observação = models.CharField(max_length=45)
    pf_ou_pj = models.CharField(max_length=15)

    class Meta:
        
        db_table = 'professor'


class Relatorio(models.Model):
    solicitação = models.OneToOneField('Solicitao', models.DO_NOTHING, primary_key=True, unique=True)  # The composite primary key (solicitação_id, controle_pagamento_id, controle_pagamento_solicitação_id) found, that is not supported. The first column is selected.
    controle_pagamento = models.ForeignKey(ControlePagamento, models.DO_NOTHING)
    controle_pagamento_solicitação = models.ForeignKey(ControlePagamento, models.DO_NOTHING, to_field='solicitação_id', related_name='relatrio_controle_pagamento_solicitação_set')

    class Meta:
        db_table = 'relatório'
        unique_together = (('solicitação', 'controle_pagamento', 'controle_pagamento_solicitação'),)


class Solicitao(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=45)
    parecer_coordenação = models.TextField()
    parecer_secretaria = models.TextField()
    parecer_compras = models.TextField()
    pendências = models.TextField()
    evento_sige = models.CharField(max_length=45)
    processo = models.CharField(max_length=45)
    solicitante = models.CharField(max_length=45)
    data_inicio = models.DateField()
    data_término = models.DateField()
    horário_inicio = models.TimeField()
    horário_término = models.TimeField()
    carga_horaria = models.IntegerField()
    valor_hora = models.FloatField()
    prestador = models.CharField(max_length=45)
    curso_treinamento = models.CharField(max_length=45)
    serviço = models.TextField()
    observação = models.TextField()

    class Meta:
        
        db_table = 'solicitação'


class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    número_telefone = models.CharField(max_length=45)
    senha = models.CharField(max_length=45)

    class Meta:
        
        db_table = 'usuario'
