# Generated by Django 4.2.15 on 2024-09-08 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0019_customuser_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='imagem',
            field=models.ImageField(blank=True, upload_to='media/users'),
        ),
    ]