# Generated by Django 4.2.15 on 2024-11-04 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0050_pedido_carrinho_alter_anuncio_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='carrinho',
        ),
        migrations.AddField(
            model_name='pedido',
            name='produtos',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Carrinho_pedido', to='bond.produto_carrinho'),
            preserve_default=False,
        ),
    ]
