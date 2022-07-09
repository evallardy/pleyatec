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
    forma_pago = models.IntegerField("Estatus",choices=STATUS_FORMA_PAGO,default=0)
    banco = models.ForeignKey(Banco,verbose_name="Banco",on_delete=models.CASCADE, null=True, blank=True)
    cuenta = models.CharField("Número de cuenta",max_length=4, null=True, blank=True, default="")
    numero_comprobante = models.CharField("Número de comprobante",max_length=40, null=True, blank=True, default="")
    estatus_pago = models.IntegerField("Estatus de pago",choices=STATUS_PAGO,default=1)
    foto_voucher = models.ImageField(upload_to="vouchers", blank=True, null=True,default=" ")
    created = models.DateTimeField("Creado", auto_now_add=True, null=True, blank=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='pg_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True, null=True, blank=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='pg_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    deposito = models.IntegerField("Depósito", choices=STATUS_DEPOSITO, default=0)
    pagado_vencido = models.IntegerField("Pagado vencido", choices=STATUS_PAGADO_VENCIDO, default=0)
    

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
                    ('nuvole_inluye_comprob_mensual', 'Nuvole Incluir comprobante de mensualidad'),
                    ('nuvole_confirma_deposito_mensual', 'Nuvole Confirma depósito mensualidad'),
                    ('nuvole_confirma_deposito_pago', 'Nuvole Confirma depósito pago'),
            # Toscana
                    ('toscana_listado_registro_mensual', 'Toscana listado registro mensualidades'),
                    ('toscana_estado_cuenta', 'Toscana Mostrar estado de cuenta'),
                    ('toscana_cap_dep_mensual', 'Toscana capturar depósito mensualidad'),
                    ('toscana_imp_estado_cuenta', 'Toscana imprime estado de cuenta'),
                    ('toscana_inluye_comprob_mensual', 'Toscana Incluir comprobante de mensualidad'),
                    ('toscana_confirma_deposito_mensual', 'Toscana Confirma depósito mensualidad'),
                    ('toscana_confirma_deposito_pago', 'Toscana Confirma depósito pago'),
            # Local Punta Oriente
                    ('local_punta_o_listado_registro_mensual', 'Local Punta O listado registro mensualidades'),
                    ('local_punta_o_estado_cuenta', 'Local Punta O Mostrar estado de cuenta'),
                    ('local_punta_o_cap_dep_mensual', 'Local Punta O capturar depósito mensualidad'),
                    ('local_punta_o_imp_estado_cuenta', 'Local Punta O imprime estado de cuenta'),
                    ('local_punta_o_inluye_comprob_mensual', 'Local Punta O Incluir comprobante de mensualidad'),
                    ('local_punta_o_confirma_deposito_mensual', 'Local Punta O Confirma depósito mensualidad'),
                    ('local_punta_o_confirma_deposito_pago', 'Local Punta O Confirma depósito pago'),
            # Consultorio Punta Oriente
                    ('consul_punta_o_listado_registro_mensual', 'Consultorio Punta O listado registro mensualidades'),
                    ('consul_punta_o_estado_cuenta', 'Consultorio Punta O Mostrar estado de cuenta'),
                    ('consul_punta_o_cap_dep_mensual', 'Consultorio Punta O capturar depósito mensualidad'),
                    ('consul_punta_o_imp_estado_cuenta', 'Consultorio Punta O imprime estado de cuenta'),
                    ('consul_punta_o_inluye_comprob_mensual', 'Consultorio Punta O Incluir comprobante de mensualidad'),
                    ('consul_punta_o_confirma_deposito_mensual', 'Consultorio Punta O Confirma depósito mensualidad'),
                    ('consul_punta_o_confirma_deposito_pago', 'Consultorio Punta O Confirma depósito pago'),
            #  Torre Vento
                    ('torre_vento_listado_registro_mensual', 'Torre Vento listado registro mensualidades'),
                    ('torre_vento_estado_cuenta', 'Torre Vento Mostrar estado de cuenta'),
                    ('torre_vento_cap_dep_mensual', 'Torre Vento capturar depósito mensualidad'),
                    ('torre_vento_imp_estado_cuenta', 'Torre Vento imprime estado de cuenta'),
                    ('torre_vento_inluye_comprob_mensual', 'Torre Vento Incluir comprobante de mensualidad'),
                    ('torre_vento_confirma_deposito_mensual', 'Torre Vento Confirma depósito mensualidad'),
                    ('torre_vento_confirma_deposito_pago', 'Torre Vento Confirma depósito pago'),
            #  Fracción 34
                    ('fraccion34_listado_registro_mensual', 'Fracción 34 listado registro mensualidades'),
                    ('fraccion34_estado_cuenta', 'Fracción 34 Mostrar estado de cuenta'),
                    ('fraccion34_cap_dep_mensual', 'Fracción 34 capturar depósito mensualidad'),
                    ('fraccion34_imp_estado_cuenta', 'Fracción 34 imprime estado de cuenta'),
                    ('fraccion34_inluye_comprob_mensual', 'Fracción 34 Incluir comprobante de mensualidad'),
                    ('fraccion34_confirma_deposito_mensual', 'Fracción 34 Confirma depósito mensualidad'),
                    ('fraccion34_confirma_deposito_pago', 'Fracción 34 Confirma depósito pago'),
            #  Vivienda Nuvole
                    ('vivienda_nuvole_listado_registro_mensual', 'Vivienda Nuvole listado registro mensualidades'),
                    ('vivienda_nuvole_estado_cuenta', 'Vivienda Nuvole Mostrar estado de cuenta'),
                    ('vivienda_nuvole_cap_dep_mensual', 'Vivienda Nuvole capturar depósito mensualidad'),
                    ('vivienda_nuvole_imp_estado_cuenta', 'Vivienda Nuvole imprime estado de cuenta'),
                    ('vivienda_nuvole_inluye_comprob_mensual', 'Vivienda Nuvole Incluir comprobante de mensualidad'),
                    ('vivienda_nuvole_confirma_deposito_mensual', 'Vivienda Nuvole Confirma depósito mensualidad'),
                    ('vivienda_nuvole_confirma_deposito_pago', 'Vivienda Nuvole Confirma depósito pago'),
            #  Pathe
                    ('pathe_listado_registro_mensual', 'Pathe listado registro mensualidades'),
                    ('pathe_estado_cuenta', 'Pathe Mostrar estado de cuenta'),
                    ('pathe_cap_dep_mensual', 'Pathe capturar depósito mensualidad'),
                    ('pathe_imp_estado_cuenta', 'Pathe imprime estado de cuenta'),
                    ('pathe_inluye_comprob_mensual', 'Pathe Incluir comprobante de mensualidad'),
                    ('pathe_confirma_deposito_mensual', 'Pathe Confirma depósito mensualidad'),
                    ('pathe_confirma_deposito_pago', 'Pathe Confirma depósito pago'),
            #  Condominio Múltiple
                    ('condom_multiple_listado_registro_mensual', 'Condominio Múltiple listado registro mensualidades'),
                    ('condom_multiple_estado_cuenta', 'Condominio Múltiple Mostrar estado de cuenta'),
                    ('condom_multiple_cap_dep_mensual', 'Condominio Múltiple capturar depósito mensualidad'),
                    ('condom_multiple_imp_estado_cuenta', 'Condominio Múltiple imprime estado de cuenta'),
                    ('condom_multiple_inluye_comprob_mensual', 'Condominio Múltiple Incluir comprobante de mensualidad'),
                    ('condom_multiple_confirma_deposito_mensual', 'Condominio Múltiple Confirma depósito mensualidad'),
                    ('condom_multiple_confirma_deposito_pago', 'Condominio Múltiple Confirma depósito pago'),
                    )

    def __str__(self):   
        return '%s, %s, %s, %s, %s, fecha_voucher:%s' % (self.id, self.convenio, self.numero_pago, self.fecha_pago, self.fecha_pago, self.fecha_voucher)

    def _get_pago_real(self):
        if self.pago_realizado == True:
            return '%s' % (self.convenio)
        else:
            return '%s' % (self.convenio)
    pago_real = property(_get_pago_real)
