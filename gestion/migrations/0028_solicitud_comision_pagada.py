# Generated by Django 3.2.4 on 2022-07-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0027_solicitud_fecha_confirma_pago_adicional'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='comision_pagada',
            field=models.IntegerField(choices=[(False, 'No'), (True, 'Si')], default=0, verbose_name='Comision pagada'),
        ),
    ]
