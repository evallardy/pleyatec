# Generated by Django 4.0.4 on 2022-05-31 20:59

import django.contrib.auth.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('paterno', models.CharField(max_length=30, verbose_name='Paterno')),
                ('materno', models.CharField(blank=True, default=' ', max_length=30, null=True, verbose_name='Materno')),
                ('nombre_conyuge', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombre coyugue')),
                ('paterno_conyuge', models.CharField(blank=True, max_length=30, null=True, verbose_name='Paterno coyugue')),
                ('materno_conyuge', models.CharField(blank=True, max_length=30, null=True, verbose_name='Materno coyugue')),
                ('rfc', models.CharField(blank=True, max_length=20, null=True, verbose_name='R.F.C.')),
                ('curp', models.CharField(blank=True, max_length=18, null=True, verbose_name='CURP')),
                ('fecha_nac', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('E', 'Empresa')], max_length=1, null=True, verbose_name='Género')),
                ('estado_civil', models.SmallIntegerField(blank=True, choices=[(1, 'Soltero'), (2, 'Casado'), (3, 'Unión libre'), (4, 'Divorciado')], null=True, verbose_name='Estado civil')),
                ('calle', models.CharField(blank=True, max_length=250, null=True, verbose_name='Calle y núm.')),
                ('colonia', models.CharField(blank=True, max_length=200, null=True, verbose_name='Colonia')),
                ('codpos', models.CharField(blank=True, max_length=5, null=True, verbose_name='Código Postal')),
                ('municipio', models.CharField(blank=True, max_length=150, null=True, verbose_name='Municipio')),
                ('estado', models.SmallIntegerField(blank=True, choices=[(0, 'Sin Estado'), (1, 'Aguascalientes'), (2, 'Baja California'), (3, 'Baja California Sur'), (4, 'Campeche'), (5, 'Coahuila'), (6, 'Colima'), (7, 'Chiapas'), (8, 'Chihuahua'), (9, 'Ciudad de México'), (10, 'Durango'), (11, 'Guanajuato'), (12, 'Guerrero'), (13, 'Hidalgo'), (14, 'Jalisco'), (15, 'México'), (16, 'Michoacán'), (17, 'Morelos'), (18, 'Nayarit'), (19, 'Nuevo León'), (20, 'Oaxaca'), (21, 'Puebla'), (22, 'Querétaro'), (23, 'Quintana Roo'), (24, 'San Luis Potosí'), (25, 'Sinaloa'), (26, 'Sonora'), (27, 'Tabasco'), (28, 'Tamaulipas'), (29, 'Tlaxcala'), (30, 'Veracruz'), (31, 'Yucatán'), (32, 'Zacatecas')], default=0, null=True, verbose_name='Estado')),
                ('telefono_fijo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefono fijo')),
                ('celular', models.CharField(blank=True, max_length=10, null=True, verbose_name='Celular')),
                ('correo', models.EmailField(blank=True, max_length=180, null=True, verbose_name='Correo')),
                ('estatus_cliente', models.SmallIntegerField(choices=[(1, 'Activo'), (2, 'Baja')], default=1, verbose_name='Activo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'Cliente',
                'ordering': ['paterno', 'materno', 'nombre'],
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
    ]
