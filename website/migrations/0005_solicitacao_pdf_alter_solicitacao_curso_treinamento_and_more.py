# Generated by Django 5.1.7 on 2025-04-01 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_professor_observacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacao',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='historico_pdfs/'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='curso_treinamento',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='prestador',
            field=models.CharField(max_length=255),
        ),
    ]
