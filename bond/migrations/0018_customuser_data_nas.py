# Generated by Django 4.2.15 on 2024-09-08 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0017_customuser_sobre'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='data_nas',
            field=models.DateTimeField(default='2001-08-03'),
            preserve_default=False,
        ),
    ]