# Generated by Django 3.2.4 on 2022-08-03 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bien', '0044_auto_20220802_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagocomision',
            name='proyecto_pago',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bien.proyecto', verbose_name='Proyecto_pag_com'),
            preserve_default=False,
        ),
    ]