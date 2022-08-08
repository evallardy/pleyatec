# Generated by Django 3.2.4 on 2022-08-08 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0048_auto_20220804_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacionamiento',
            name='compartido',
            field=models.IntegerField(choices=[(1, 'No'), (2, 'Si')], default=1, verbose_name='Compartido'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='comision_pagada',
            field=models.IntegerField(choices=[(1, 'No'), (2, 'Si')], default=1, verbose_name='Comision pagada'),
        ),
    ]
