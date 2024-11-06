# Generated by Django 4.2.15 on 2024-11-02 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bond', '0048_transacao_status_alter_anuncio_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('valor_antigo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditos_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_carrinho', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.CharField(choices=[('Pendente', 'Pendente'), ('Concluida', 'Concluida'), ('Recusada', 'Recusada')], max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_remetente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rementente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='creditos',
            name='user',
        ),
        migrations.RenameField(
            model_name='extrato',
            old_name='quantidade',
            new_name='valor_carrinho',
        ),
        migrations.RemoveField(
            model_name='extrato',
            name='user_destino',
        ),
        migrations.AddField(
            model_name='extrato',
            name='carrinho',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='carrinho_extrato', to='bond.carrinho'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Transacao',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='creditos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditosCustom', to='bond.credito'),
        ),
        migrations.DeleteModel(
            name='Creditos',
        ),
    ]