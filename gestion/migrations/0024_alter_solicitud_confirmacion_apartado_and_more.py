# Generated by Django 4.0.4 on 2022-07-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0023_alter_solicitud_confirmacion_apartado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='confirmacion_apartado',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Sin confirmar'), (2, 'Confirmado')], default=0, verbose_name='Depósito apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='confirmacion_pago_adicional',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Sin confirmar'), (2, 'Confirmado')], default=0, verbose_name='Depósito PA'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='forma_pago_apa',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Cheque'), (2, 'Transferencia'), (3, 'Efectivo')], default=0, verbose_name='Forma pago apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='forma_pago_pa',
            field=models.IntegerField(choices=[(0, '---------'), (1, 'Cheque'), (2, 'Transferencia'), (3, 'Efectivo')], default=0, verbose_name='Forma pago pago adic.'),
        ),
    ]
