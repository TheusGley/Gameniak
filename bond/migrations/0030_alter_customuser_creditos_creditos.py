# Generated by Django 4.2.15 on 2024-10-08 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bond', '0029_alter_mensagem_manager_user_env_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='creditos',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.CreateModel(
            name='Creditos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantia', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditos_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
