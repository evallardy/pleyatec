# Generated by Django 3.2.4 on 2022-08-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0043_auto_20220802_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagocomision',
            name='fecha_alta',
        ),
        migrations.RemoveField(
            model_name='pagocomision',
            name='fecha_cierre',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_alta',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha alta proyecto'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_cierre',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha cierre proyecto'),
        ),
    ]
