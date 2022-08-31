# Generated by Django 4.0.4 on 2022-08-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0067_alter_lote_manzana_alter_lote_nivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='estacionamientos',
            field=models.IntegerField(default=0, verbose_name='Estacionamientos'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_circulo_x',
            field=models.IntegerField(default=0, verbose_name='Posición X circulo'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_circulo_y',
            field=models.IntegerField(default=0, verbose_name='Posición Y circulo'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_texto_x',
            field=models.IntegerField(default=0, verbose_name='Posición X mts'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_texto_y',
            field=models.IntegerField(default=0, verbose_name='Posición Y mts'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_x',
            field=models.IntegerField(default=0, verbose_name='Posición X numero'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='posicion_y',
            field=models.IntegerField(default=0, verbose_name='Posición Y numero'),
        ),
    ]
