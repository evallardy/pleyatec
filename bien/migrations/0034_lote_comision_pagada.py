# Generated by Django 3.2.4 on 2022-07-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0033_auto_20220722_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote',
            name='comision_pagada',
            field=models.IntegerField(choices=[(False, 'No'), (True, 'Si')], default=0, verbose_name='Comision pagada'),
        ),
    ]
