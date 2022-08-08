# Generated by Django 3.2.4 on 2022-08-08 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0031_auto_20220808_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='asigna_descuento',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False, verbose_name='Asigna descuento'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='comision_pagada',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False, verbose_name='Comision pagada'),
        ),
    ]
