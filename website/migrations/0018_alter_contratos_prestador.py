# Generated by Django 5.2 on 2025-05-11 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_alter_professor_cnpj_alter_professor_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratos',
            name='prestador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.professor'),
        ),
    ]
