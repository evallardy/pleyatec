# Generated by Django 4.0.4 on 2022-07-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0030_alter_pago_options_alter_pago_deposito'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='deposito',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Sin confirmar'), (2, 'Confirmado')], default=1, verbose_name='Depósito'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='forma_pago',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Cheque'), (2, 'Transferencia'), (3, 'Efectivo')], default=0, verbose_name='Estatus'),
        ),
    ]