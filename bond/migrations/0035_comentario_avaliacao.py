# Generated by Django 4.2.15 on 2024-10-10 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0034_comentario_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='avaliacao',
            field=models.IntegerField(default=0),
        ),
    ]