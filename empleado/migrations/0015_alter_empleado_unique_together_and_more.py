# Generated by Django 4.0.4 on 2022-08-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleado', '0014_alter_empleado_estado_civil'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='empleado',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='calle_num',
            field=models.CharField(default=' ', max_length=250, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='celular',
            field=models.CharField(default=' ', max_length=10, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='codpos',
            field=models.CharField(default=' ', max_length=5, verbose_name='Código Postal'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='colonia',
            field=models.CharField(default=' ', max_length=200, verbose_name='Colonia'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='cuenta_banco',
            field=models.CharField(default=' ', max_length=18, verbose_name='Cuenta nómina'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='curp',
            field=models.CharField(default=' ', max_length=18, verbose_name='CURP'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='estado',
            field=models.IntegerField(choices=[(0, 'Sin Estado'), (1, 'Aguascalientes'), (2, 'Baja California'), (3, 'Baja California Sur'), (4, 'Campeche'), (5, 'Coahuila'), (6, 'Colima'), (7, 'Chiapas'), (8, 'Chihuahua'), (9, 'Ciudad de México'), (10, 'Durango'), (11, 'Guanajuato'), (12, 'Guerrero'), (13, 'Hidalgo'), (14, 'Jalisco'), (15, 'México'), (16, 'Michoacán'), (17, 'Morelos'), (18, 'Nayarit'), (19, 'Nuevo León'), (20, 'Oaxaca'), (21, 'Puebla'), (22, 'Querétaro'), (23, 'Quintana Roo'), (24, 'San Luis Potosí'), (25, 'Sinaloa'), (26, 'Sonora'), (27, 'Tabasco'), (28, 'Tamaulipas'), (29, 'Tlaxcala'), (30, 'Veracruz'), (31, 'Yucatán'), (32, 'Zacatecas')], default=0, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='materno',
            field=models.CharField(default=' ', max_length=30, verbose_name='Materno'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='municipio',
            field=models.CharField(default=' ', max_length=150, verbose_name='Municipio'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='numero_seguro_social',
            field=models.CharField(default=' ', max_length=12, verbose_name='Número de seguro social'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='rfc',
            field=models.CharField(default=' ', max_length=20, verbose_name='R.F.C.'),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='telefono_fijo',
            field=models.CharField(default=' ', max_length=50, verbose_name='Telefono fijo'),
        ),
    ]
