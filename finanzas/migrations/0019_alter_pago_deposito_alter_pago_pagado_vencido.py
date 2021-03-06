# Generated by Django 4.0.4 on 2022-07-03 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0018_alter_pago_pagado_vencido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='deposito',
            field=models.BooleanField(blank=True, choices=[(0, 'Sin confirmar'), (1, 'Confirmado')], default=False, null=True, verbose_name='Depósito confirmado'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='pagado_vencido',
            field=models.BooleanField(blank=True, choices=[(0, 'Normal'), (1, 'Vencido')], default=False, null=True, verbose_name='Pagado vencido'),
        ),
    ]
