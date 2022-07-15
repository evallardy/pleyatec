# Generated by Django 4.0.4 on 2022-07-10 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0019_alter_solicitud_confirmacion_apartado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='foto_comprobante_apartado',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='comp_apartado'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='foto_comprobante_pago_adicional',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='comp_adicional'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='confirmacion_apartado',
            field=models.IntegerField(choices=[(1, 'Sin confirmar'), (2, 'Confirmado')], default=1, verbose_name='Depósito apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='confirmacion_pago_adicional',
            field=models.IntegerField(choices=[(1, 'Sin confirmar'), (2, 'Confirmado')], default=1, verbose_name='Depósito PA'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='foto_acta_const',
            field=models.ImageField(blank=True, default=' ', null=True, upload_to='acte_const'),
        ),
    ]
