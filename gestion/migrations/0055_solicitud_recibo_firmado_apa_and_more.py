# Generated by Django 4.0.4 on 2023-02-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0054_alter_solicitud_anio_inicio_pago_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='recibo_firmado_apa',
            field=models.FileField(blank=True, null=True, upload_to='compApartado/firmado', verbose_name='Recibo firmado apartado'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='recibo_firmado_pa',
            field=models.FileField(blank=True, null=True, upload_to='compAdicional/firmado', verbose_name='Recibo firmado pago adic'),
        ),
    ]
