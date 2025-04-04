# Generated by Django 5.1.7 on 2025-03-24 05:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_usuario_email_alter_usuario_numero_telefone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='cnpj',
            field=models.CharField(blank=True, max_length=18, null=True, validators=[django.core.validators.RegexValidator(regex='/^[0-9]{2}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[\\/]?[0-9]{4}[-]?[0-9]{2}$/')]),
        ),
        migrations.AddField(
            model_name='professor',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(regex='([0-9]{2}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[\\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[-]?[0-9]{2})')]),
        ),
    ]
