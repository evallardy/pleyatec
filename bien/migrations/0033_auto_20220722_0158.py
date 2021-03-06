# Generated by Django 3.2.4 on 2022-07-22 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0032_auto_20220722_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='comision_asesor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Comision Asesor'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='comision_jefe_asesor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Comision jefe Asesor'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='bien_anexo',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Anexo del bien'),
        ),
    ]
