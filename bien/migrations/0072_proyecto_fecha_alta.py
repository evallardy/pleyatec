# Generated by Django 4.0.4 on 2022-08-29 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0071_alter_pagocomision_enganche'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='fecha_alta',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha cierre proyecto'),
        ),
    ]
