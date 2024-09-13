# Generated by Django 4.2.15 on 2024-09-08 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0010_transaction_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('Depósito', 'Depósito'), ('Compra', 'Compra')], max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.customuser')),
            ],
        ),
    ]