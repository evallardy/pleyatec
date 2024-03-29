# Generated by Django 3.2.4 on 2022-08-08 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0049_auto_20220808_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacionamiento',
            name='compartido',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Si')], default=1, verbose_name='Compartido'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='comision_pagada',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Si')], default=1, verbose_name='Comision pagada'),
        ),
    ]
