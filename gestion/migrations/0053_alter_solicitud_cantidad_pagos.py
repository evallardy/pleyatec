# Generated by Django 4.0.4 on 2022-10-05 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0052_alter_solicitud_calle_alter_solicitud_celular_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='cantidad_pagos',
            field=models.IntegerField(default=0, verbose_name='Pagos'),
        ),
    ]
