# Generated by Django 4.2.15 on 2024-10-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0031_alter_customuser_creditos'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='avaliacao',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
