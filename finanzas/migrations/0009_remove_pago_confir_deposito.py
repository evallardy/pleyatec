# Generated by Django 4.0.4 on 2022-07-01 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0008_pago_deposito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pago',
            name='confir_deposito',
        ),
    ]
