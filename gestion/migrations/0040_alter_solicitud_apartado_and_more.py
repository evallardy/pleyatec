# Generated by Django 4.0.4 on 2022-08-27 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0039_regla_valor11_alter_regla_valor1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='apartado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='aprobacion_director',
            field=models.SmallIntegerField(choices=[(0, 'No'), (1, 'Si')], default=0, verbose_name='Aprobación director desarrollo'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='aprobacion_gerente',
            field=models.SmallIntegerField(choices=[(0, 'No'), (1, 'Si')], default=0, verbose_name='Aprobación gerente de ventas'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='cuenta_apa',
            field=models.CharField(default=' ', max_length=4, verbose_name='Número de cuenta apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='cuenta_pa',
            field=models.CharField(default='', max_length=4, verbose_name='Número de cuenta pago adic'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='enganche',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Enganche'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='foto_comprobante_apartado',
            field=models.FileField(blank=True, null=True, upload_to='compApartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='foto_comprobante_pago_adicional',
            field=models.FileField(blank=True, null=True, upload_to='compAdicional'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='foto_elector_frente',
            field=models.FileField(default=' ', upload_to='ine'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='importe_x_pago',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Importe por pago'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='numero_comprobante_apa',
            field=models.CharField(default=' ', max_length=40, verbose_name='Número de comprobante apartado'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='numero_comprobante_pa',
            field=models.CharField(default='', max_length=40, verbose_name='Número de comprobante pago adic'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='pago_adicional',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Pago adicional'),
        ),
    ]
