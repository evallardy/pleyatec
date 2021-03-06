# Generated by Django 4.0.4 on 2022-06-02 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0004_alter_lote_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='esquina',
            field=models.BooleanField(choices=[(False, ''), (True, 'Si')], default=False, verbose_name='Esquina'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='tipo_lote',
            field=models.BooleanField(default=True, verbose_name='Tipo de lote'),
        ),
    ]
