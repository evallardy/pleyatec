# Generated by Django 4.0.4 on 2022-06-02 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0006_alter_lote_tipo_lote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='altura',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='esquina',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Si')], default=0, verbose_name='Esquina'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='estacionamientos',
            field=models.IntegerField(default=0, verbose_name='Estacionamientos'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='precio_x_mt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio por m²'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='terraza',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Terraza m²'),
        ),
    ]
