# Generated by Django 4.0.4 on 2022-07-01 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0011_pago_pagado_vencido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='cuenta',
            field=models.CharField(blank=True, default='', max_length=4, null=True, verbose_name='Número de cuenta'),
        ),
    ]
