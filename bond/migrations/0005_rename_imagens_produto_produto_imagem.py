# Generated by Django 4.2.15 on 2024-08-31 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0004_alter_banner_imagem1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='imagens_produto',
            new_name='imagem',
        ),
    ]
