# Generated by Django 4.0.4 on 2022-05-31 20:59

import django.contrib.auth.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleado', '0001_initial'),
        ('cliente', '0001_initial'),
        ('bien', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_lote', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio lote')),
                ('precio_final', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio final')),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Descuento')),
                ('modo_pago', models.IntegerField(choices=[(1, 'Contado'), (2, 'Crédito directo'), (3, 'Crédito hipotecario'), (4, 'Contado a crédito')], default=1, verbose_name='Modo de pago')),
                ('enganche', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Enganche')),
                ('pago_adicional', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Pago adicional')),
                ('apartado', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Apartado')),
                ('cantidad_pagos', models.IntegerField(blank=True, default=0, null=True, verbose_name='Pagos')),
                ('importe_x_pago', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Importe por pago')),
                ('aprobacion_gerente', models.BooleanField(default=False, verbose_name='Aprobación gerente de ventas')),
                ('aprobacion_director', models.BooleanField(default=False, verbose_name='Aprobación director desarrollo')),
                ('foto_elector_frente', models.ImageField(blank=True, default=' ', null=True, upload_to='documentos')),
                ('foto_elector_reverso', models.ImageField(blank=True, default=' ', null=True, upload_to='documentos')),
                ('foto_matrimonio', models.ImageField(blank=True, default=' ', null=True, upload_to='documentos')),
                ('foto_comprobante', models.ImageField(blank=True, default=' ', null=True, upload_to='documentos')),
                ('num_apartado', models.IntegerField(blank=True, default=0, null=True, verbose_name='Recibo apartado')),
                ('num_adicional', models.IntegerField(blank=True, default=0, null=True, verbose_name='Recibo adicional')),
                ('num_contrato', models.IntegerField(blank=True, default=0, null=True, verbose_name='Número de contrato')),
                ('pagos_pagados', models.IntegerField(blank=True, default=0, null=True, verbose_name='Pagos realizados')),
                ('importe_pagado', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Importe pagado')),
                ('asigna_descuento', models.BooleanField(blank=True, default=False, null=True, verbose_name='Asigna descuento')),
                ('porcentaje_descuento', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Descuento')),
                ('fecha_contrato', models.DateField(blank=True, null=True, verbose_name='Fecha de contrato')),
                ('mes_inicio_pago', models.DecimalField(blank=True, choices=[(0, '-----'), (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], decimal_places=0, default=0, max_digits=2, null=True, verbose_name='Mes de inicio de pago')),
                ('anio_inicio_pago', models.DecimalField(blank=True, choices=[(0, '-----'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'), (2025, '2025')], decimal_places=0, default=0, max_digits=4, null=True, verbose_name='Año de inicio de pago')),
                ('estatus_solicitud', models.IntegerField(choices=[(1, 'Nueva'), (2, 'Apartado de lote'), (3, 'Comprometida'), (4, 'Pagando a crédito'), (5, 'Reasignar'), (6, 'Terminada'), (7, 'Archivo-Terminada'), (8, 'Archivo-Cancelada'), (9, 'Contado, con datos de contrato'), (10, 'Pagando a crédito, con datos de contrato'), (99, 'Cancelada')], default=1, verbose_name='Estatus')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('asesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleado.empleado', verbose_name='Asesor')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente', verbose_name='Cliente')),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bien.lote', verbose_name='Lote')),
                ('usuario_ins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sl_user_ins', to='empleado.empleado', verbose_name='Usuario insertó')),
                ('usuario_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sl_user_mod', to='empleado.empleado', verbose_name='Usuario modificó')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
                'db_table': 'Solicitud',
                'ordering': ['id'],
                'permissions': (('autoriza_visualiza', 'Ver autorizaciones'), ('autoriza_venta', 'Autoriza solicitud por Gerente ventas'), ('autoriza_desarrollo', 'Autoriza solicitud por Director desarrollo'), ('consulta_archivo', 'Consultar el histórico de solicitudes'), ('compromiso', 'Realiza compromiso de compra'), ('creditos', 'Consulta contratos a crédito'), ('contados', 'Consulta contratos de contado'), ('check_pagos', 'Check list de pagos'), ('pago_compromiso', 'Realizar pago compromiso'), ('contratar', 'Generar contrato'), ('datos_contrato', 'Incluir datos al contrato'), ('imprime_contrato', 'Impresión de contrato'), ('archivar_contrato', 'Archivar contrato'), ('amortizacion', 'Listado de amortización'), ('imprime_amortizacion', 'Imprime listado de amortización')),
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
        migrations.CreateModel(
            name='Folios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Recibo pago terreno'), (2, 'Contrato'), (3, 'Comisiones'), (4, 'Facturas'), (5, 'Remisiones')], default=1, verbose_name='Tipo folio')),
                ('numero', models.IntegerField(verbose_name='Número')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de entrega')),
                ('observacion', models.CharField(max_length=200, verbose_name='Observación')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Importe recibo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('estatus_folio', models.IntegerField(choices=[(1, 'Activo'), (9, 'Cancelado')], default=1, verbose_name='Estatus')),
                ('usuario_ins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fl_user_ins', to='empleado.empleado', verbose_name='Usuario insertó')),
                ('usuario_mod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fl_user_mod', to='empleado.empleado', verbose_name='Usuario modificó')),
            ],
            options={
                'verbose_name': 'Folio',
                'verbose_name_plural': 'Folios',
                'db_table': 'Folio',
                'ordering': ['tipo', 'numero'],
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
    ]