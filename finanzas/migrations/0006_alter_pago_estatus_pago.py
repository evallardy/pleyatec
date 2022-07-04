# Generated by Django 4.0.4 on 2022-06-30 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_pago_pago_realizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='estatus_pago',
            field=models.IntegerField(choices=[(1, 'Vigente'), (2, 'Pagado'), (99, 'Cancelado')], default=1, verbose_name='Estatus de pago'),
        ),
    ]