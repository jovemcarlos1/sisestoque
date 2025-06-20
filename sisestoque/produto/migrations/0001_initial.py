# Generated by Django 5.2 on 2025-05-06 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cor', models.CharField(max_length=200, verbose_name='Cor')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', models.CharField(max_length=200, verbose_name='Produto')),
                ('descricao', models.TextField(blank=True, verbose_name='Descriçao')),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('preco', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Preço')),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Modificado em')),
                ('cor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produto.cores', verbose_name='Cor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['-produto'],
            },
        ),
    ]
