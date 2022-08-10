# Generated by Django 3.2.4 on 2022-08-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0052_auto_20220808_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagocomision',
            name='estatus_pago_comision',
            field=models.IntegerField(choices=[(0, 'Nueva'), (1, 'Desositada'), (2, 'Recibida')], default=0, verbose_name='Estatus comisión aasesor'),
        ),
        migrations.AlterField(
            model_name='pagocomision',
            name='estatus_pago_gerente',
            field=models.IntegerField(choices=[(0, 'Nueva'), (1, 'Desositada'), (2, 'Recibida')], default=0, verbose_name='Estatus comisión director'),
        ),
        migrations.AlterField(
            model_name='pagocomision',
            name='estatus_pago_publicidad',
            field=models.IntegerField(choices=[(0, 'Nueva'), (1, 'Desositada'), (2, 'Recibida')], default=0, verbose_name='Estatus comisión director'),
        ),
    ]