# Generated by Django 4.2.15 on 2024-10-10 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0035_comentario_avaliacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='data_create',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
