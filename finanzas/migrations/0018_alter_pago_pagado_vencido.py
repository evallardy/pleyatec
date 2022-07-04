# Generated by Django 4.0.4 on 2022-07-03 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0017_alter_pago_estatus_pago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='pagado_vencido',
            field=models.BooleanField(choices=[(0, 'Normal'), (1, 'Vencido')], default=False, verbose_name='Pagado vencido'),
        ),
    ]