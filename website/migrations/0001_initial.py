# Generated by Django 5.1.7 on 2025-03-10 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ControlePagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situação_pasta', models.CharField(max_length=45)),
                ('data_inicio', models.DateField()),
                ('data_termino', models.DateField()),
                ('modalidade', models.CharField(max_length=45)),
                ('curso_componentes', models.CharField(max_length=45)),
                ('evento', models.CharField(max_length=45)),
                ('solicitante', models.CharField(max_length=45)),
                ('fornecedor', models.CharField(max_length=45)),
                ('valor_sc', models.FloatField()),
                ('total_horas_contradas', models.IntegerField()),
                ('valor_hora_aula', models.FloatField()),
                ('valor_pago', models.FloatField()),
                ('saldo', models.FloatField()),
                ('saldo_de_horas', models.IntegerField()),
                ('horas_pagas', models.IntegerField()),
                ('prazo_validade_contrato', models.DateField()),
                ('observação', models.TextField()),
            ],
            options={
                'db_table': 'controle_pagamento',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'login',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=45)),
                ('data_nascimento', models.DateField()),
                ('observação', models.CharField(max_length=45)),
                ('pf_ou_pj', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'professor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Solicitao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=45)),
                ('parecer_coordenação', models.TextField()),
                ('parecer_secretaria', models.TextField()),
                ('parecer_compras', models.TextField()),
                ('pendências', models.TextField()),
                ('evento_sige', models.CharField(max_length=45)),
                ('processo', models.CharField(max_length=45)),
                ('solicitante', models.CharField(max_length=45)),
                ('data_inicio', models.DateField()),
                ('data_término', models.DateField()),
                ('horário_inicio', models.TimeField()),
                ('horário_término', models.TimeField()),
                ('carga_horaria', models.IntegerField()),
                ('valor_hora', models.FloatField()),
                ('prestador', models.CharField(max_length=45)),
                ('curso_treinamento', models.CharField(max_length=45)),
                ('serviço', models.TextField()),
                ('observação', models.TextField()),
            ],
            options={
                'db_table': 'solicitação',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=255)),
                ('número_telefone', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
    ]
