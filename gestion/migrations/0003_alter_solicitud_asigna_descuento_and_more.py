# Generated by Django 4.0.4 on 2022-06-06 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_alter_solicitud_asigna_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='asigna_descuento',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=False, verbose_name='Asigna descuento'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='modo_pago',
            field=models.IntegerField(choices=[(1, 'Contado'), (2, 'Crédito directo'), (4, 'Contado a crédito')], default=1, verbose_name='Modo de pago'),
        ),
    ]
