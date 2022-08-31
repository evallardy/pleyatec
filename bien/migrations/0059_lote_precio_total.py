# Generated by Django 4.0.4 on 2022-08-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0058_alter_lote_comision_pagada'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='precio_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Precio total'),
        ),
    ]
