# Generated by Django 4.0.4 on 2022-08-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0008_remove_cliente_usuario_ins_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='regimen',
            field=models.SmallIntegerField(choices=[(0, 'Bienes separados'), (1, 'Bienes mancomunados')], default=0, verbose_name='Régime'),
        ),
    ]