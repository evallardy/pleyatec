# Generated by Django 4.0.4 on 2022-06-29 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_remove_cliente_telefono_fijo_cliente_razon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=1, verbose_name='Género'),
        ),
    ]