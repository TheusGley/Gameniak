# Generated by Django 4.2.15 on 2024-10-17 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0042_comentario_servico_alter_comentario_produto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servico',
            old_name='imagens_produto',
            new_name='imagem',
        ),
    ]
