# Generated by Django 4.0.4 on 2022-09-03 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0049_alter_solicitud_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='celular',
            field=models.CharField(default=' ', max_length=20, verbose_name='Celular'),
        ),
    ]
