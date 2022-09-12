from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from empleado.models import *
from gestion.models import *

class Pago(models.Model, PermissionRequiredMixin):
    convenio = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='num_conv1',
        verbose_name="Convenio")
    numero_pago = models.IntegerField("Número de pago",default=0)
    fecha_pago = models.DateField("Fecha de pago", null=True, blank=True)
    importe = models.DecimalField("Importe", decimal_places=2, max_digits=10,default=0.0)
    fecha_voucher = models.DateField("Fecha de voucher", null=True, blank=True)
    importe_pagado = models.DecimalField("Importe_pagado", decimal_places=2, max_digits=10,default=0.0)
    fecha_pago_moratorio = models.DateField("Fecha pago de moratorio", null=True, blank=True)
    moratorio = models.DecimalField("Interés moratorio", decimal_places=2, max_digits=10,default=0.0)
    forma_pago = models.IntegerField("Forma de pago",choices=STATUS_FORMA_PAGO,default=0)
    banco = models.ForeignKey(Banco,verbose_name="Banco",on_delete=models.CASCADE, null=True, blank=True)
    cuenta = models.CharField("Número de cuenta",max_length=4, null=True, blank=True, default=" ")
    numero_comprobante = models.CharField("Número de comprobante",max_length=40, default=" ")
    estatus_pago = models.IntegerField("Estatus de pago",choices=STATUS_PAGO,default=1)
    file_comprobante = models.FileField(upload_to="comprobante", blank=True, null=True,default=" ")
    created = models.DateTimeField("Creado", auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True, null=True, blank=True)
    deposito = models.IntegerField("Depósito", choices=STATUS_DEPOSITO, default=1)
    pagado_vencido = models.IntegerField("Pagado vencido", choices=STATUS_PAGADO_VENCIDO, default=0)
    folio_recibo = models.IntegerField('Folio de pago mensual',default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['convenio', 'numero_pago'], name="%(app_label)s_%(class)s_unique")
        ]

    class Meta:
        verbose_name = 'Pagos'
        verbose_name_plural = 'Pago'
        ordering = ['id']
        db_table = 'Pago'
        permissions = (
            # Nuvole
                    ('nuvole_listado_registro_mensual', 'Nuvole listado registro mensualidades'),
                    ('nuvole_estado_cuenta', 'Nuvole Mostrar estado de cuenta'),
                    ('nuvole_cap_dep_mensual', 'Nuvole capturar depósito mensualidad'),
                    ('nuvole_imp_estado_cuenta', 'Nuvole imprime estado de cuenta'),
                    ('nuvole_imprime_comprob_mensual', 'Nuvole imprimir comprobante de mensual'),
                    ('nuvole_confirma_deposito_mensual', 'Nuvole Confirma depósito mensualidad'),
                    ('nuvole_confirma_deposito_pago', 'Nuvole Confirma depósito pago'),
                    ('nuvole_ver_comisiones', 'Nuvole ver comisiones'),
                    ('nuvole_edita_comisiones_proyecto', 'Nuvole edita comisiones proyecto'),
                    ('nuvole_pago_normal_comisiones', 'Nuvole pago normal comisiones'),
                    ('nuvole_pago_extemp_comisiones', 'Nuvole pago extemp comisiones'),
                    ('nuvole_consulta_comisiones', 'Nuvole consulta comisiones'),
                    ('nuvole_vobo_comisiones', 'Nuvole vobo comisiones'),
            # Toscana
                    ('toscana_listado_registro_mensual', 'Toscana listado registro mensualidades'),
                    ('toscana_estado_cuenta', 'Toscana Mostrar estado de cuenta'),
                    ('toscana_cap_dep_mensual', 'Toscana capturar depósito mensualidad'),
                    ('toscana_imp_estado_cuenta', 'Toscana imprime estado de cuenta'),
                    ('toscana_imprime_comprob_mensual', 'Toscana imprimir comprobante de mensual'),
                    ('toscana_confirma_deposito_mensual', 'Toscana Confirma depósito mensualidad'),
                    ('toscana_confirma_deposito_pago', 'Toscana Confirma depósito pago'),
                    ('toscana_ver_comisiones', 'Toscana ver comisiones'),
                    ('toscana_edita_comisiones_proyecto', 'Toscana edita comisiones proyecto'),
                    ('toscana_pago_normal_comisiones', 'Toscana pago normal comisiones'),
                    ('toscana_pago_extemp_comisiones', 'Toscana pago extemp comisiones'),
                    ('toscana_consulta_comisiones', 'Toscana consulta comisiones'),
                    ('toscana_vobo_comisiones', 'Toscana vobo comisiones'),
            # Local Punta Oriente
                    ('local_punta_o_listado_registro_mensual', 'Local Punta O listado registro mensualidades'),
                    ('local_punta_o_estado_cuenta', 'Local Punta O Mostrar estado de cuenta'),
                    ('local_punta_o_cap_dep_mensual', 'Local Punta O capturar depósito mensualidad'),
                    ('local_punta_o_imp_estado_cuenta', 'Local Punta O imprime estado de cuenta'),
                    ('local_punta_o_imprime_comprob_mensual', 'Local Punta O imprimir comprobante de mensual'),
                    ('local_punta_o_confirma_deposito_mensual', 'Local Punta O Confirma depósito mensualidad'),
                    ('local_punta_o_confirma_deposito_pago', 'Local Punta O Confirma depósito pago'),
                    ('local_punta_o_ver_comisiones', 'Local Punta O ver comisiones'),
                    ('local_punta_o_edita_comisiones_proyecto', 'Local Punta O edita comisiones proyecto'),
                    ('local_punta_o_pago_normal_comisiones', 'Local Punta O pago normal comisiones'),
                    ('local_punta_o_pago_extemp_comisiones', 'Local Punta O pago extemp comisiones'),
                    ('local_punta_o_consulta_comisiones', 'Local Punta O consulta comisiones'),
                    ('local_punta_o_vobo_comisiones', 'Local Punta O vobo comisiones'),
            # Consultorio Punta Oriente
                    ('consul_punta_o_listado_registro_mensual', 'Consultorio Punta O listado registro mensualidades'),
                    ('consul_punta_o_estado_cuenta', 'Consultorio Punta O Mostrar estado de cuenta'),
                    ('consul_punta_o_cap_dep_mensual', 'Consultorio Punta O capturar depósito mensualidad'),
                    ('consul_punta_o_imp_estado_cuenta', 'Consultorio Punta O imprime estado de cuenta'),
                    ('consul_punta_o_imprime_comprob_mensual', 'Consultorio Punta O imprimir comprobante de mensual'),
                    ('consul_punta_o_confirma_deposito_mensual', 'Consultorio Punta O Confirma depósito mensualidad'),
                    ('consul_punta_o_confirma_deposito_pago', 'Consultorio Punta O Confirma depósito pago'),
                    ('consul_punta_o_ver_comisiones', 'Consultorio Punta O ver comisiones'),
                    ('consul_punta_o_edita_comisiones_proyecto', 'Consultorio Punta O edita comisiones proyecto'),
                    ('consul_punta_o_pago_normal_comisiones', 'Consultorio Punta O pago normal comisiones'),
                    ('consul_punta_o_pago_extemp_comisiones', 'Consultorio Punta O pago extemp comisiones'),
                    ('consul_punta_o_consulta_comisiones', 'Consultorio Punta O consulta comisiones'),
                    ('consul_punta_o_vobo_comisiones', 'Consultorio Punta O vobo comisiones'),
            #  Torre Vento
                    ('torre_vento_listado_registro_mensual', 'Torre Vento listado registro mensualidades'),
                    ('torre_vento_estado_cuenta', 'Torre Vento Mostrar estado de cuenta'),
                    ('torre_vento_cap_dep_mensual', 'Torre Vento capturar depósito mensualidad'),
                    ('torre_vento_imp_estado_cuenta', 'Torre Vento imprime estado de cuenta'),
                    ('torre_vento_imprime_comprob_mensual', 'Torre Vento imprimir comprobante de mensual'),
                    ('torre_vento_confirma_deposito_mensual', 'Torre Vento Confirma depósito mensualidad'),
                    ('torre_vento_confirma_deposito_pago', 'Torre Vento Confirma depósito pago'),
                    ('torre_vento_ver_comisiones', 'Torre Vento ver comisiones'),
                    ('torre_vento_edita_comisiones_proyecto', 'Torre Vento edita comisiones proyecto'),
                    ('torre_vento_pago_normal_comisiones', 'Torre Vento pago normal comisiones'),
                    ('torre_vento_pago_extemp_comisiones', 'Torre Vento pago extemp comisiones'),
                    ('torre_vento_consulta_comisiones', 'Torre Vento consulta comisiones'),
                    ('torre_vento_vobo_comisiones', 'Torre Vento vobo comisiones'),
            #  Porto Santo
                    ('porto_santo_listado_registro_mensual', 'Porto Santo listado registro mensualidades'),
                    ('porto_santo_estado_cuenta', 'Porto Santo Mostrar estado de cuenta'),
                    ('porto_santo_cap_dep_mensual', 'Porto Santo capturar depósito mensualidad'),
                    ('porto_santo_imp_estado_cuenta', 'Porto Santo imprime estado de cuenta'),
                    ('porto_santo_imprime_comprob_mensual', 'Porto Santo imprimir comprobante de mensual'),
                    ('porto_santo_confirma_deposito_mensual', 'Porto Santo Confirma depósito mensualidad'),
                    ('porto_santo_confirma_deposito_pago', 'Porto Santo Confirma depósito pago'),
                    ('porto_santo_ver_comisiones', 'Porto Santo ver comisiones'),
                    ('porto_santo_edita_comisiones_proyecto', 'Porto Santo edita comisiones proyecto'),
                    ('porto_santo_pago_normal_comisiones', 'Porto Santo pago normal comisiones'),
                    ('porto_santo_pago_extemp_comisiones', 'Porto Santo pago extemp comisiones'),
                    ('porto_santo_consulta_comisiones', 'Porto Santo consulta comisiones'),
                    ('porto_santo_vobo_comisiones', 'Porto Santo vobo comisiones'),
            #  Vivienda Nuvole
                    ('vivienda_nuvole_listado_registro_mensual', 'Vivienda Nuvole listado registro mensualidades'),
                    ('vivienda_nuvole_estado_cuenta', 'Vivienda Nuvole Mostrar estado de cuenta'),
                    ('vivienda_nuvole_cap_dep_mensual', 'Vivienda Nuvole capturar depósito mensualidad'),
                    ('vivienda_nuvole_imp_estado_cuenta', 'Vivienda Nuvole imprime estado de cuenta'),
                    ('vivienda_nuvole_imprime_comprob_mensual', 'Vivienda Nuvole imprimir comprobante de mensual'),
                    ('vivienda_nuvole_confirma_deposito_mensual', 'Vivienda Nuvole Confirma depósito mensualidad'),
                    ('vivienda_nuvole_confirma_deposito_pago', 'Vivienda Nuvole Confirma depósito pago'),
                    ('vivienda_nuvole_ver_comisiones', 'Vivienda Nuvole ver comisiones'),
                    ('vivienda_nuvole_edita_comisiones_proyecto', 'Vivienda Nuvole edita comisiones proyecto'),
                    ('vivienda_nuvole_pago_normal_comisiones', 'Vivienda Nuvole pago normal comisiones'),
                    ('vivienda_nuvole_pago_extemp_comisiones', 'Vivienda Nuvole pago extemp comisiones'),
                    ('vivienda_nuvole_consulta_comisiones', 'Vivienda Nuvole consulta comisiones'),
                    ('vivienda_nuvole_vobo_comisiones', 'Vivienda Nuvole vobo comisiones'),
            #  Monte Cristallo
                    ('monte_cristallo_listado_registro_mensual', 'Monte Cristallo listado registro mensualidades'),
                    ('monte_cristallo_estado_cuenta', 'Monte Cristallo Mostrar estado de cuenta'),
                    ('monte_cristallo_cap_dep_mensual', 'Monte Cristallo capturar depósito mensualidad'),
                    ('monte_cristallo_imp_estado_cuenta', 'Monte Cristallo imprime estado de cuenta'),
                    ('monte_cristallo_imprime_comprob_mensual', 'Monte Cristallo imprimir comprobante de mensual'),
                    ('monte_cristallo_confirma_deposito_mensual', 'Monte Cristallo Confirma depósito mensualidad'),
                    ('monte_cristallo_confirma_deposito_pago', 'Monte Cristallo Confirma depósito pago'),
                    ('monte_cristallo_ver_comisiones', 'Monte Cristallo ver comisiones'),
                    ('monte_cristallo_edita_comisiones_proyecto', 'Monte Cristallo edita comisiones proyecto'),
                    ('monte_cristallo_pago_normal_comisiones', 'Monte Cristallo pago normal comisiones'),
                    ('monte_cristallo_pago_extemp_comisiones', 'Monte Cristallo pago extemp comisiones'),
                    ('monte_cristallo_consulta_comisiones', 'Monte Cristallo consulta comisiones'),
                    ('monte_cristallo_vobo_comisiones', 'Monte Cristallo vobo comisiones'),
            #  Condominio Múltiple
                    ('condom_multiple_listado_registro_mensual', 'Condominio Múltiple listado registro mensualidades'),
                    ('condom_multiple_estado_cuenta', 'Condominio Múltiple Mostrar estado de cuenta'),
                    ('condom_multiple_cap_dep_mensual', 'Condominio Múltiple capturar depósito mensualidad'),
                    ('condom_multiple_imp_estado_cuenta', 'Condominio Múltiple imprime estado de cuenta'),
                    ('condom_multiple_imprime_comprob_mensual', 'Condominio Múltiple imprimir comprobante de mensual'),
                    ('condom_multiple_confirma_deposito_mensual', 'Condominio Múltiple Confirma depósito mensualidad'),
                    ('condom_multiple_confirma_deposito_pago', 'Condominio Múltiple Confirma depósito pago'),
                    ('condom_multiple_ver_comisiones', 'Condominio Múltiple ver comisiones'),
                    ('condom_multiple_edita_comisiones_proyecto', 'Condominio Múltiple edita comisiones proyecto'),
                    ('condom_multiple_pago_normal_comisiones', 'Condominio Múltiple pago normal comisiones'),
                    ('condom_multiple_pago_extemp_comisiones', 'Condominio Múltiple pago extemp comisiones'),
                    ('condom_multiple_consulta_comisiones', 'Condominio Múltiple consulta comisiones'),
                    ('condom_multiple_vobo_comisiones', 'Condominio Múltiple vobo comisiones'),
                    )

    def __str__(self):   
        return '%s, %s, %s, %s, %s, fecha_voucher:%s' % (self.id, self.convenio, self.numero_pago, self.fecha_pago, self.fecha_pago, self.fecha_voucher)

    def _get_pago_real(self):
        if self.pago_realizado == True:
            return '%s' % (self.convenio)
        else:
            return '%s' % (self.convenio)
    pago_real = property(_get_pago_real)
