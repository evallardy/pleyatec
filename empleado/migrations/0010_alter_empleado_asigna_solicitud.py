# Generated by Django 3.2.4 on 2022-08-08 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0009_alter_empleado_estatus_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='asigna_solicitud',
            field=models.IntegerField(blank=True, choices=[(1, 'No'), (2, 'Si')], default=1, null=True, verbose_name='Asigna solicitudes'),
        ),
    ]
