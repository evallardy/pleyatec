# Generated by Django 3.2.4 on 2022-08-08 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0034_auto_20220807_2356'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pago',
            options={'ordering': ['id'], 'permissions': (('nuvole_listado_registro_mensual', 'Nuvole listado registro mensualidades'), ('nuvole_estado_cuenta', 'Nuvole Mostrar estado de cuenta'), ('nuvole_cap_dep_mensual', 'Nuvole capturar depósito mensualidad'), ('nuvole_imp_estado_cuenta', 'Nuvole imprime estado de cuenta'), ('nuvole_inluye_comprob_mensual', 'Nuvole Incluir comprobante de mensualidad'), ('nuvole_confirma_deposito_mensual', 'Nuvole Confirma depósito mensualidad'), ('nuvole_confirma_deposito_pago', 'Nuvole Confirma depósito pago'), ('nuvole_ver_comisiones', 'Nuvole ver comisiones'), ('nuvole_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('nuvole_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('nuvole_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('nuvole_consulta_comisiones', 'Nuvole consulta comisiones'), ('toscana_listado_registro_mensual', 'Toscana listado registro mensualidades'), ('toscana_estado_cuenta', 'Toscana Mostrar estado de cuenta'), ('toscana_cap_dep_mensual', 'Toscana capturar depósito mensualidad'), ('toscana_imp_estado_cuenta', 'Toscana imprime estado de cuenta'), ('toscana_inluye_comprob_mensual', 'Toscana Incluir comprobante de mensualidad'), ('toscana_confirma_deposito_mensual', 'Toscana Confirma depósito mensualidad'), ('toscana_confirma_deposito_pago', 'Toscana Confirma depósito pago'), ('toscana_ver_comisiones', 'Nuvole ver comisiones'), ('toscana_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('toscana_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('toscana_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('toscana_consulta_comisiones', 'Nuvole consulta comisiones'), ('local_punta_o_listado_registro_mensual', 'Local Punta O listado registro mensualidades'), ('local_punta_o_estado_cuenta', 'Local Punta O Mostrar estado de cuenta'), ('local_punta_o_cap_dep_mensual', 'Local Punta O capturar depósito mensualidad'), ('local_punta_o_imp_estado_cuenta', 'Local Punta O imprime estado de cuenta'), ('local_punta_o_inluye_comprob_mensual', 'Local Punta O Incluir comprobante de mensualidad'), ('local_punta_o_confirma_deposito_mensual', 'Local Punta O Confirma depósito mensualidad'), ('local_punta_o_confirma_deposito_pago', 'Local Punta O Confirma depósito pago'), ('local_punta_o_ver_comisiones', 'Nuvole ver comisiones'), ('local_punta_o_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('local_punta_o_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('local_punta_o_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('local_punta_o_consulta_comisiones', 'Nuvole consulta comisiones'), ('consul_punta_o_listado_registro_mensual', 'Consultorio Punta O listado registro mensualidades'), ('consul_punta_o_estado_cuenta', 'Consultorio Punta O Mostrar estado de cuenta'), ('consul_punta_o_cap_dep_mensual', 'Consultorio Punta O capturar depósito mensualidad'), ('consul_punta_o_imp_estado_cuenta', 'Consultorio Punta O imprime estado de cuenta'), ('consul_punta_o_inluye_comprob_mensual', 'Consultorio Punta O Incluir comprobante de mensualidad'), ('consul_punta_o_confirma_deposito_mensual', 'Consultorio Punta O Confirma depósito mensualidad'), ('consul_punta_o_confirma_deposito_pago', 'Consultorio Punta O Confirma depósito pago'), ('consul_punta_o_ver_comisiones', 'Nuvole ver comisiones'), ('consul_punta_o_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('consul_punta_o_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('consul_punta_o_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('consul_punta_o_consulta_comisiones', 'Nuvole consulta comisiones'), ('torre_vento_listado_registro_mensual', 'Torre Vento listado registro mensualidades'), ('torre_vento_estado_cuenta', 'Torre Vento Mostrar estado de cuenta'), ('torre_vento_cap_dep_mensual', 'Torre Vento capturar depósito mensualidad'), ('torre_vento_imp_estado_cuenta', 'Torre Vento imprime estado de cuenta'), ('torre_vento_inluye_comprob_mensual', 'Torre Vento Incluir comprobante de mensualidad'), ('torre_vento_confirma_deposito_mensual', 'Torre Vento Confirma depósito mensualidad'), ('torre_vento_confirma_deposito_pago', 'Torre Vento Confirma depósito pago'), ('torre_vento_ver_comisiones', 'Nuvole ver comisiones'), ('torre_vento_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('torre_vento_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('torre_vento_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('torre_vento_consulta_comisiones', 'Nuvole consulta comisiones'), ('porto_santo_listado_registro_mensual', 'Fracción 34 listado registro mensualidades'), ('porto_santo_estado_cuenta', 'Fracción 34 Mostrar estado de cuenta'), ('porto_santo_cap_dep_mensual', 'Fracción 34 capturar depósito mensualidad'), ('porto_santo_imp_estado_cuenta', 'Fracción 34 imprime estado de cuenta'), ('porto_santo_inluye_comprob_mensual', 'Fracción 34 Incluir comprobante de mensualidad'), ('porto_santo_confirma_deposito_mensual', 'Fracción 34 Confirma depósito mensualidad'), ('porto_santo_confirma_deposito_pago', 'Fracción 34 Confirma depósito pago'), ('porto_santo_ver_comisiones', 'Nuvole ver comisiones'), ('porto_santo_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('porto_santo_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('porto_santo_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('porto_santo_consulta_comisiones', 'Nuvole consulta comisiones'), ('vivienda_nuvole_listado_registro_mensual', 'Vivienda Nuvole listado registro mensualidades'), ('vivienda_nuvole_estado_cuenta', 'Vivienda Nuvole Mostrar estado de cuenta'), ('vivienda_nuvole_cap_dep_mensual', 'Vivienda Nuvole capturar depósito mensualidad'), ('vivienda_nuvole_imp_estado_cuenta', 'Vivienda Nuvole imprime estado de cuenta'), ('vivienda_nuvole_inluye_comprob_mensual', 'Vivienda Nuvole Incluir comprobante de mensualidad'), ('vivienda_nuvole_confirma_deposito_mensual', 'Vivienda Nuvole Confirma depósito mensualidad'), ('vivienda_nuvole_confirma_deposito_pago', 'Vivienda Nuvole Confirma depósito pago'), ('vivienda_nuvole_ver_comisiones', 'Nuvole ver comisiones'), ('vivienda_nuvole_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('vivienda_nuvole_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('vivienda_nuvole_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('vivienda_nuvole_consulta_comisiones', 'Nuvole consulta comisiones'), ('monte_cristalo_listado_registro_mensual', 'Monte cristalo listado registro mensualidades'), ('monte_cristalo_estado_cuenta', 'Monte cristalo Mostrar estado de cuenta'), ('monte_cristalo_cap_dep_mensual', 'Monte cristalo capturar depósito mensualidad'), ('monte_cristalo_imp_estado_cuenta', 'Monte cristalo imprime estado de cuenta'), ('monte_cristalo_inluye_comprob_mensual', 'Monte cristalo Incluir comprobante de mensualidad'), ('monte_cristalo_confirma_deposito_mensual', 'Monte cristalo Confirma depósito mensualidad'), ('monte_cristalo_confirma_deposito_pago', 'Monte cristalo Confirma depósito pago'), ('monte_cristalo_ver_comisiones', 'Nuvole ver comisiones'), ('monte_cristalo_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('monte_cristalo_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('monte_cristalo_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('monte_cristalo_consulta_comisiones', 'Nuvole consulta comisiones'), ('condom_multiple_listado_registro_mensual', 'Condominio Múltiple listado registro mensualidades'), ('condom_multiple_estado_cuenta', 'Condominio Múltiple Mostrar estado de cuenta'), ('condom_multiple_cap_dep_mensual', 'Condominio Múltiple capturar depósito mensualidad'), ('condom_multiple_imp_estado_cuenta', 'Condominio Múltiple imprime estado de cuenta'), ('condom_multiple_inluye_comprob_mensual', 'Condominio Múltiple Incluir comprobante de mensualidad'), ('condom_multiple_confirma_deposito_mensual', 'Condominio Múltiple Confirma depósito mensualidad'), ('condom_multiple_confirma_deposito_pago', 'Condominio Múltiple Confirma depósito pago'), ('condom_multiple_ver_comisiones', 'Nuvole ver comisiones'), ('condom_multiple_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'), ('condom_multiple_pago_normal_comisiones', 'Nuvole pago normal comisiones'), ('condom_multiple_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'), ('condom_multiple_consulta_comisiones', 'Nuvole consulta comisiones')), 'verbose_name': 'Pagos', 'verbose_name_plural': 'Pago'},
        ),
    ]
