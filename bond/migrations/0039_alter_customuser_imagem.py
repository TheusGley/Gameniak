# Generated by Django 4.2.15 on 2024-10-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0038_rename_imagem_comentario_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]
