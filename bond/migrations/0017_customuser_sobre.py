# Generated by Django 4.2.15 on 2024-09-08 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0016_alter_credittransaction_user_alter_order_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='sobre',
            field=models.CharField(default='Matheus ', max_length=200),
            preserve_default=False,
        ),
    ]
