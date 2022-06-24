# Generated by Django 4.0.4 on 2022-06-13 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='cuenta',
            field=models.CharField(blank=True, default='', max_length=25, null=True, verbose_name='Número de cuenta'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='estatus_pago',
            field=models.IntegerField(choices=[(1, 'Vigente'), (2, 'Vencido'), (3, 'Pagado'), (99, 'Cancelado')], default=1, verbose_name='Estatus de pago'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='forma_pago',
            field=models.IntegerField(choices=[(0, '-----'), (1, 'Cheque'), (2, 'Transferencia'), (3, 'Efectivo')], default=0, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='numero_comprobante',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='Número de comprobante'),
        ),
    ]
