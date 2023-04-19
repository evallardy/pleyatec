# Generated by Django 4.0.4 on 2023-04-18 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0043_alter_pago_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='importe_original',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Importe_pagado'),
        ),
    ]
