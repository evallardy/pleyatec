# Generated by Django 4.0.4 on 2022-07-13 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0021_solicitud_cuenta_apa_solicitud_cuenta_pa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='foto_comprobante_apartado',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='compApartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='foto_comprobante_pago_adicional',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='compAdicional'),
        ),
    ]
