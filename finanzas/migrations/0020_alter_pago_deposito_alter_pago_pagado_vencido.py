# Generated by Django 4.0.4 on 2022-07-03 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0019_alter_pago_deposito_alter_pago_pagado_vencido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='deposito',
            field=models.IntegerField(blank=True, choices=[(0, 'Sin confirmar'), (1, 'Confirmado')], default=0, null=True, verbose_name='Depósito confirmado'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='pagado_vencido',
            field=models.IntegerField(blank=True, choices=[(0, 'Normal'), (1, 'Vencido')], default=0, null=True, verbose_name='Pagado vencido'),
        ),
    ]