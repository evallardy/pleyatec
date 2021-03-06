# Generated by Django 4.0.4 on 2022-05-31 20:59

import django.contrib.auth.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestion', '0001_initial'),
        ('core', '0002_initial'),
        ('empleado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_pago', models.IntegerField(default=0, verbose_name='Número de pago')),
                ('fecha_pago', models.DateField(blank=True, null=True, verbose_name='Fecha de pago')),
                ('importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Importe')),
                ('fecha_pago_moratorio', models.DateField(blank=True, null=True, verbose_name='Fecha pago de moratorio')),
                ('moratorio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Interés moratorio')),
                ('forma_pago', models.IntegerField(choices=[(1, 'Cheque'), (2, 'Transferencia'), (3, 'Efectivo')], default=1, verbose_name='Estatus')),
                ('cuenta', models.CharField(blank=True, max_length=25, null=True, verbose_name='Número de cuenta')),
                ('numero_comprobante', models.IntegerField(default=0, verbose_name='Número de comprobante')),
                ('estatus_pago', models.IntegerField(choices=[(1, 'Aplicado'), (2, 'Pendiente'), (99, 'Cancelado')], default=1, verbose_name='Estatus de pago')),
                ('foto_voucher', models.ImageField(blank=True, default=' ', null=True, upload_to='vouchers')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creado')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Actualizado')),
                ('banco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.banco', verbose_name='Banco')),
                ('convenio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='num_conv1', to='gestion.solicitud', verbose_name='Convenio')),
                ('usuario_ins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pg_user_ins', to='empleado.empleado', verbose_name='Usuario insertó')),
                ('usuario_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pg_user_mod', to='empleado.empleado', verbose_name='Usuario modificó')),
            ],
            options={
                'verbose_name': 'Pagos',
                'verbose_name_plural': 'Pago',
                'db_table': 'Pago',
                'ordering': ['id'],
                'permissions': (('estado_cuenta', 'Mostrar estado de cuenta'), ('listado_pagos', 'Mostrar listado de pagos'), ('comprobante_pagos', 'Incluir comprobante de pago')),
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
    ]
