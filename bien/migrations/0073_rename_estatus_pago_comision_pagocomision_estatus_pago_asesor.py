# Generated by Django 4.0.4 on 2022-09-06 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0072_proyecto_fecha_alta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagocomision',
            old_name='estatus_pago_comision',
            new_name='estatus_pago_asesor',
        ),
    ]
