# Generated by Django 4.2.15 on 2024-08-31 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0003_remove_banner_imagem2_remove_banner_imagem3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='imagem1',
            field=models.ImageField(blank=True, null=True, upload_to='media/banners'),
        ),
    ]
