# Generated by Django 4.0.4 on 2023-02-22 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0041_pago_recibo_firmado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='pagado_vencido',
            field=models.IntegerField(choices=[(1, 'A tiempo'), (2, 'Vencido')], default=0, verbose_name='Pagado vencido'),
        ),
    ]
