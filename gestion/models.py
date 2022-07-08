from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.funciones import fecha_hoy
from core.models import *
from cliente.models import *
from bien.models import *

from django.template.defaultfilters import date, default
from django.utils.timezone import now
from django.db.models import AutoField
from django.contrib.auth.models import User
import datetime

cyear = datetime.date.today().year
cmonth = datetime.date.today().month
hoy = fecha_hoy()

class Solicitud(models.Model, PermissionRequiredMixin):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, verbose_name="Lote")
    asesor = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Asesor")
    precio_lote = models.DecimalField("Precio lote", decimal_places=2, max_digits=10, default=0)
    precio_final = models.DecimalField("Precio final", decimal_places=2, max_digits=10, default=0)
    tipo_descuento = models.IntegerField("Asigna descuento",choices=TIPO_DESCUENTO, default=1)
    porcentaje_descuento = models.DecimalField("Porcentaje desc.", decimal_places=2, max_digits=4, default=0, null=True, blank=True)
    descuento = models.DecimalField("Descuento", decimal_places=2, max_digits=10, default=0)
    modo_pago = models.IntegerField("Modo de pago",choices=MODO_PAGO,default=1)
    enganche = models.DecimalField("Enganche", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    pago_adicional = models.DecimalField("Pago adicional", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    confirmacion_pago_adicional = models.IntegerField("Depósito", choices=STATUS_DEPOSITO, default=0)
    apartado = models.DecimalField("Apartado", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    confirmacion_apartado = models.IntegerField("Depósito", choices=STATUS_DEPOSITO, default=0)
    cantidad_pagos = models.IntegerField("Pagos", null=True, blank=True, default=0)
    importe_x_pago = models.DecimalField("Importe por pago", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    aprobacion_gerente = models.BooleanField("Aprobación gerente de ventas", default=False)
    aprobacion_director = models.BooleanField("Aprobación director desarrollo", default=False)
    foto_elector_frente = models.ImageField(upload_to="ine", blank=True, null=True,default=" ")
    foto_elector_reverso = models.ImageField(upload_to="ine", blank=True, null=True,default=" ")
    foto_elector_frente_cy = models.ImageField(upload_to="ine_cy", blank=True, null=True,default=" ")
    foto_elector_reverso_cy = models.ImageField(upload_to="ine_cy", blank=True, null=True,default=" ")
    foto_matrimonio = models.ImageField(upload_to="matrimonio", blank=True, null=True,default=" ")
    foto_comprobante = models.ImageField(upload_to="comprobante", blank=True, null=True,default=" ")
    foto_alta_shcp = models.ImageField(upload_to="alta_shcp", blank=True, null=True,default=" ")
    foto_acta_const = models.ImageField(upload_to="acte_cont", blank=True, null=True,default=" ")
    num_apartado = models.IntegerField("Recibo apartado", blank=True, null=True, default=0)
    num_adicional = models.IntegerField("Recibo adicional", blank=True, null=True, default=0)
    num_contrato = models.IntegerField("Número de contrato", blank=True, null=True, default=0)
    pagos_pagados = models.IntegerField("Pagos realizados", default=0, blank=True, null=True)
    importe_pagado = models.DecimalField("Importe pagado", decimal_places=2, max_digits=10, default=0, blank=True, null=True)
    asigna_descuento = models.BooleanField("Asigna descuento",choices=RESP_SI_NO, default=False)
    porcentaje_descuento = models.DecimalField("Descuento", decimal_places=2, max_digits=5, default=0, blank=True, null=True)
    fecha_contrato = models.DateField("Fecha de contrato", blank=True, null=True)
    mes_inicio_pago = models.DecimalField("Mes de inicio de pago", choices=MESES, decimal_places=0, max_digits=2, blank=True, null=True, default=0)
    anio_inicio_pago = models.DecimalField("Año de inicio de pago", choices=ANIOS, decimal_places=0, max_digits=4, blank=True, null=True, default=0)
    estatus_solicitud = models.IntegerField("Estatus",choices=STATUS_SOLICITUD,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='sl_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='sl_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    tipo_cliente = models.BooleanField("Tipo de cliente", choices=TIPO_CLIENTE, default=False)
    razon = models.CharField("Razón social",max_length=255, blank=True, default=" ")
    nombre = models.CharField("Nombre",max_length=30, null=True, blank=True)
    paterno = models.CharField("Paterno",max_length=30, null=True, blank=True, default=" ")
    materno = models.CharField("Materno",max_length=30, null=True, blank=True, default=" ")
    nombre_conyuge = models.CharField("Nombre coyugue",max_length=30, null=True, blank=True)
    paterno_conyuge = models.CharField("Paterno coyugue",max_length=30, null=True, blank=True)
    materno_conyuge = models.CharField("Materno coyugue",max_length=30, null=True, blank=True)
    rfc = models.CharField("R.F.C.",max_length=20, blank=True, null=True)
    curp = models.CharField("CURP",max_length=18, null=True, blank=True)
    estado_civil = models.SmallIntegerField("Estado civil", choices=ESTADO_CIVIL, null=True, blank=True)
    regimen = models.BooleanField("Régime", choices=REGIMEN, null=True, blank=True)
    calle = models.CharField("Calle y núm.",max_length=250, blank=True, null=True)
    colonia = models.CharField("Colonia",max_length=200, blank=True, null=True)
    codpos = models.CharField("Código Postal",max_length=5, blank=True, null=True)
    municipio = models.CharField("Municipio",max_length=150, blank=True, null=True)
    estado = models.SmallIntegerField("Estado",choices=ESTADOS, blank=True, null=True, default=0)
    celular = models.CharField("Celular", max_length=10, blank=True, null=True)
    correo = models.EmailField("Correo", max_length=180, blank=True, null=True)

    class Meta:
        verbose_name = 'Solicitud' 
        verbose_name_plural = 'Solicitudes' 
        ordering = ['id']
        db_table = 'Solicitud'
        permissions = (
            # Nuvole
                        ('nuvole_ver_solicitud', 'Nuvole Listado ver solicitudes'),
                        ('nuvole_add_solicitud', 'Nuvole agrega solicitud'),
                        ('nuvole_cambia_solicitud', 'Nuvole cambia solicitud'),
                        ('nuvole_cancela_solicitud', 'Nuvole cancela solicitud'),
                        ('nuvole_asigna_descto', 'Nuvole asigna descto solicitud'),
                        ('nuvole_amortizac', 'Nuvole Listado de amortización'),
                        ('nuvole_imprime_amortizac', 'Nuvole Imprime listado de amortización'),
                        ('nuvole_autoriza_visualiza', 'Nuvole Ver autorizaciones'),
                        ('nuvole_autoriza_venta', 'Nuvole Autoriza solicitud por Gerente ventas'),
                        ('nuvole_autoriza_desarrollo', 'Nuvole Autoriza solicitud por Director desarrollo'),
                        ('nuvole_compromiso', 'Nuvole Realiza compromiso de compra'),
                        ('nuvole_pago_compromiso', 'Nuvole Realizar pago compromiso'),
                        ('nuvole_imp_pago_compromiso', 'Nuvole imprime pago compromiso'),
                        ('nuvole_contratar', 'Nuvole Generar contrato'),
                        ('nuvole_datos_contrato', 'Nuvole Incluir datos al contrato'),
                        ('nuvole_imprime_contrato', 'Nuvole Impresión de contrato'),
                        ('nuvole_archivar_contrato', 'Nuvole Archivar contrato'),
                        ('nuvole_consulta_archivo', 'Nuvole Consultar el histórico de solicitudes'),
                        ('nuvole_creditos', 'Nuvole Consulta contratos a crédito'),
                        ('nuvole_contados', 'Nuvole Consulta contratos de contado'),
            # Toscana
                        ('toscana_ver_solicitud', 'Toscana Listado ver solicitudes'),
                        ('toscana_add_solicitud', 'Toscana agrega solicitud'),
                        ('toscana_cambia_solicitud', 'Toscana cambia solicitud'),
                        ('toscana_cancela_solicitud', 'Toscana cancela solicitud'),
                        ('toscana_asigna_descto', 'Toscana asigna descto solicitud'),
                        ('toscana_amortizac', 'Toscana Listado de amortización'),
                        ('toscana_imprime_amortizac', 'Toscana Imprime listado de amortización'),
                        ('toscana_autoriza_visualiza', 'Toscana Ver autorizaciones'),
                        ('toscana_autoriza_venta', 'Toscana Autoriza solicitud por Gerente ventas'),
                        ('toscana_autoriza_desarrollo', 'Toscana Autoriza solicitud por Director desarrollo'),
                        ('toscana_compromiso', 'Toscana Realiza compromiso de compra'),
                        ('toscana_pago_compromiso', 'Toscana Realizar pago compromiso'),
                        ('toscana_imp_pago_compromiso', 'Toscana imprime pago compromiso'),
                        ('toscana_contratar', 'Toscana Generar contrato'),
                        ('toscana_datos_contrato', 'Toscana Incluir datos al contrato'),
                        ('toscana_imprime_contrato', 'Toscana Impresión de contrato'),
                        ('toscana_archivar_contrato', 'Toscana Archivar contrato'),
                        ('toscana_consulta_archivo', 'Toscana Consultar el histórico de solicitudes'),
                        ('toscana_creditos', 'Toscana Consulta contratos a crédito'),
                        ('toscana_contados', 'Toscana Consulta contratos de contado'),
            # Local Punta Oriente
                        ('local_punta_o_ver_solicitud', 'Local Punta O Listado ver solicitudes'),
                        ('local_punta_o_add_solicitud', 'Local Punta O agrega solicitud'),
                        ('local_punta_o_cambia_solicitud', 'Local Punta O cambia solicitud'),
                        ('local_punta_o_cancela_solicitud', 'Local Punta O cancela solicitud'),
                        ('local_punta_o_asigna_descto', 'Local Punta O asigna descto solicitud'),
                        ('local_punta_o_amortizac', 'Local Punta O Listado de amortización'),
                        ('local_punta_o_imprime_amortizac', 'Local Punta O Imprime listado de amortización'),
                        ('local_punta_o_autoriza_visualiza', 'Local Punta O Ver autorizaciones'),
                        ('local_punta_o_autoriza_venta', 'Local Punta O Autoriza solicitud por Gerente ventas'),
                        ('local_punta_o_autoriza_desarrollo', 'Local Punta O Autoriza solicitud por Director desarrollo'),
                        ('local_punta_o_compromiso', 'Local Punta O Realiza compromiso de compra'),
                        ('local_punta_o_pago_compromiso', 'Local Punta O Realizar pago compromiso'),
                        ('local_punta_o_imp_pago_compromiso', 'Local Punta O imprime pago compromiso'),
                        ('local_punta_o_contratar', 'Local Punta O Generar contrato'),
                        ('local_punta_o_datos_contrato', 'Local Punta O Incluir datos al contrato'),
                        ('local_punta_o_imprime_contrato', 'Local Punta O Impresión de contrato'),
                        ('local_punta_o_archivar_contrato', 'Local Punta O Archivar contrato'),
                        ('local_punta_o_consulta_archivo', 'Local Punta O Consultar el histórico de solicitudes'),
                        ('local_punta_o_creditos', 'Local Punta O Consulta contratos a crédito'),
                        ('local_punta_o_contados', 'Local Punta O Consulta contratos de contado'),
            # Consultorio Punta Oriente
                        ('consul_punta_o_ver_solicitud', 'Consultorio Punta O Listado ver solicitudes'),
                        ('consul_punta_o_add_solicitud', 'Consultorio Punta O agrega solicitud'),
                        ('consul_punta_o_cambia_solicitud', 'Consultorio Punta O cambia solicitud'),
                        ('consul_punta_o_cancela_solicitud', 'Consultorio Punta O cancela solicitud'),
                        ('consul_punta_o_asigna_descto', 'Consultorio Punta O asigna descto solicitud'),
                        ('consul_punta_o_amortizac', 'Consultorio Punta O Listado de amortización'),
                        ('consul_punta_o_imprime_amortizac', 'Consultorio Punta O Imprime listado de amortización'),
                        ('consul_punta_o_autoriza_visualiza', 'Consultorio Punta O Ver autorizaciones'),
                        ('consul_punta_o_autoriza_venta', 'Consultorio Punta O Autoriza solicitud por Gerente ventas'),
                        ('consul_punta_o_autoriza_desarrollo', 'Consultorio Punta O Autoriza solicitud por Director desarrollo'),
                        ('consul_punta_o_compromiso', 'Consultorio Punta O Realiza compromiso de compra'),
                        ('consul_punta_o_pago_compromiso', 'Consultorio Punta O Realizar pago compromiso'),
                        ('consul_punta_o_imp_pago_compromiso', 'Consultorio Punta O imprime pago compromiso'),
                        ('consul_punta_o_contratar', 'Consultorio Punta O Generar contrato'),
                        ('consul_punta_o_datos_contrato', 'Consultorio Punta O Incluir datos al contrato'),
                        ('consul_punta_o_imprime_contrato', 'Consultorio Punta O Impresión de contrato'),
                        ('consul_punta_o_archivar_contrato', 'Consultorio Punta O Archivar contrato'),
                        ('consul_punta_o_consulta_archivo', 'Consultorio Punta O Consultar el histórico de solicitudes'),
                        ('consul_punta_o_creditos', 'Consultorio Punta O Consulta contratos a crédito'),
                        ('consul_punta_o_contados', 'Consultorio Punta O Consulta contratos de contado'),
            #  Torre Vento
                        ('torre_vento_ver_solicitud', 'Torre Vento Listado ver solicitudes'),
                        ('torre_vento_add_solicitud', 'Torre Vento agrega solicitud'),
                        ('torre_vento_cambia_solicitud', 'Torre Vento cambia solicitud'),
                        ('torre_vento_cancela_solicitud', 'Torre Vento cancela solicitud'),
                        ('torre_vento_asigna_descto', 'Torre Vento asigna descto solicitud'),
                        ('torre_vento_amortizac', 'Torre Vento Listado de amortización'),
                        ('torre_vento_imprime_amortizac', 'Torre Vento Imprime listado de amortización'),
                        ('torre_vento_autoriza_visualiza', 'Torre Vento Ver autorizaciones'),
                        ('torre_vento_autoriza_venta', 'Torre Vento Autoriza solicitud por Gerente ventas'),
                        ('torre_vento_autoriza_desarrollo', 'Torre Vento Autoriza solicitud por Director desarrollo'),
                        ('torre_vento_compromiso', 'Torre Vento Realiza compromiso de compra'),
                        ('torre_vento_pago_compromiso', 'Torre Vento Realizar pago compromiso'),
                        ('torre_vento_imp_pago_compromiso', 'Torre Vento imprime pago compromiso'),
                        ('torre_vento_contratar', 'Torre Vento Generar contrato'),
                        ('torre_vento_datos_contrato', 'Torre Vento Incluir datos al contrato'),
                        ('torre_vento_imprime_contrato', 'Torre Vento Impresión de contrato'),
                        ('torre_vento_archivar_contrato', 'Torre Vento Archivar contrato'),
                        ('torre_vento_consulta_archivo', 'Torre Vento Consultar el histórico de solicitudes'),
                        ('torre_vento_creditos', 'Torre Vento Consulta contratos a crédito'),
                        ('torre_vento_contados', 'Torre Vento Consulta contratos de contado'),
            #  Fracción 34
                        ('fraccion34_ver_solicitud', 'Fracción 34 Listado ver solicitudes'),
                        ('fraccion34_add_solicitud', 'Fracción 34 agrega solicitud'),
                        ('fraccion34_cambia_solicitud', 'Fracción 34 cambia solicitud'),
                        ('fraccion34_cancela_solicitud', 'Fracción 34 cancela solicitud'),
                        ('fraccion34_asigna_descto', 'Fracción 34 asigna descto solicitud'),
                        ('fraccion34_amortizac', 'Fracción 34 Listado de amortización'),
                        ('fraccion34_imprime_amortizac', 'Fracción 34 Imprime listado de amortización'),
                        ('fraccion34_autoriza_visualiza', 'Fracción 34 Ver autorizaciones'),
                        ('fraccion34_autoriza_venta', 'Fracción 34 Autoriza solicitud por Gerente ventas'),
                        ('fraccion34_autoriza_desarrollo', 'Fracción 34 Autoriza solicitud por Director desarrollo'),
                        ('fraccion34_compromiso', 'Fracción 34 Realiza compromiso de compra'),
                        ('fraccion34_pago_compromiso', 'Fracción 34 Realizar pago compromiso'),
                        ('fraccion34_imp_pago_compromiso', 'Fracción 34 imprime pago compromiso'),
                        ('fraccion34_contratar', 'Fracción 34 Generar contrato'),
                        ('fraccion34_datos_contrato', 'Fracción 34 Incluir datos al contrato'),
                        ('fraccion34_imprime_contrato', 'Fracción 34 Impresión de contrato'),
                        ('fraccion34_archivar_contrato', 'Fracción 34 Archivar contrato'),
                        ('fraccion34_consulta_archivo', 'Fracción 34 Consultar el histórico de solicitudes'),
                        ('fraccion34_creditos', 'Fracción 34 Consulta contratos a crédito'),
                        ('fraccion34_contados', 'Fracción 34 Consulta contratos de contado'),
            #  Vivienda Nuvole
                        ('vivienda_nuvole_ver_solicitud', 'Vivienda Nuvole Listado ver solicitudes'),
                        ('vivienda_nuvole_add_solicitud', 'Vivienda Nuvole agrega solicitud'),
                        ('vivienda_nuvole_cambia_solicitud', 'Vivienda Nuvole cambia solicitud'),
                        ('vivienda_nuvole_cancela_solicitud', 'Vivienda Nuvole cancela solicitud'),
                        ('vivienda_nuvole_asigna_descto', 'Vivienda Nuvole asigna descto solicitud'),
                        ('vivienda_nuvole_amortizac', 'Vivienda Nuvole Listado de amortización'),
                        ('vivienda_nuvole_imprime_amortizac', 'Vivienda Nuvole Imprime listado de amortización'),
                        ('vivienda_nuvole_autoriza_visualiza', 'Vivienda Nuvole Ver autorizaciones'),
                        ('vivienda_nuvole_autoriza_venta', 'Vivienda Nuvole Autoriza solicitud por Gerente ventas'),
                        ('vivienda_nuvole_autoriza_desarrollo', 'Vivienda Nuvole Autoriza solicitud por Director desarrollo'),
                        ('vivienda_nuvole_compromiso', 'Vivienda Nuvole Realiza compromiso de compra'),
                        ('vivienda_nuvole_pago_compromiso', 'Vivienda Nuvole Realizar pago compromiso'),
                        ('vivienda_nuvole_imp_pago_compromiso', 'Vivienda Nuvole imprime pago compromiso'),
                        ('vivienda_nuvole_contratar', 'Vivienda Nuvole Generar contrato'),
                        ('vivienda_nuvole_datos_contrato', 'Vivienda Nuvole Incluir datos al contrato'),
                        ('vivienda_nuvole_imprime_contrato', 'Vivienda Nuvole Impresión de contrato'),
                        ('vivienda_nuvole_archivar_contrato', 'Vivienda Nuvole Archivar contrato'),
                        ('vivienda_nuvole_consulta_archivo', 'Vivienda Nuvole Consultar el histórico de solicitudes'),
                        ('vivienda_nuvole_creditos', 'Vivienda Nuvole Consulta contratos a crédito'),
                        ('vivienda_nuvole_contados', 'Vivienda Nuvole Consulta contratos de contado'),
            #  Pathe
                        ('pathe_ver_solicitud', 'Pathe Listado ver solicitudes'),
                        ('pathe_add_solicitud', 'Pathe agrega solicitud'),
                        ('pathe_cambia_solicitud', 'Pathe cambia solicitud'),
                        ('pathe_cancela_solicitud', 'Pathe cancela solicitud'),
                        ('pathe_asigna_descto', 'Pathe asigna descto solicitud'),
                        ('pathe_amortizac', 'Pathe Listado de amortización'),
                        ('pathe_imprime_amortizac', 'Pathe Imprime listado de amortización'),
                        ('pathe_autoriza_visualiza', 'Pathe Ver autorizaciones'),
                        ('pathe_autoriza_venta', 'Pathe Autoriza solicitud por Gerente ventas'),
                        ('pathe_autoriza_desarrollo', 'Pathe Autoriza solicitud por Director desarrollo'),
                        ('pathe_compromiso', 'Pathe Realiza compromiso de compra'),
                        ('pathe_pago_compromiso', 'Pathe Realizar pago compromiso'),
                        ('pathe_imp_pago_compromiso', 'Pathe imprime pago compromiso'),
                        ('pathe_contratar', 'Pathe Generar contrato'),
                        ('pathe_datos_contrato', 'Pathe Incluir datos al contrato'),
                        ('pathe_imprime_contrato', 'Pathe Impresión de contrato'),
                        ('pathe_archivar_contrato', 'Pathe Archivar contrato'),
                        ('pathe_consulta_archivo', 'Pathe Consultar el histórico de solicitudes'),
                        ('pathe_creditos', 'Pathe Consulta contratos a crédito'),
                        ('pathe_contados', 'Pathe Consulta contratos de contado'),
            #  Condominio Múltiple
                        ('condom_multiple_ver_solicitud', 'Condominio Múltiple Listado ver solicitudes'),
                        ('condom_multiple_add_solicitud', 'Condominio Múltiple agrega solicitud'),
                        ('condom_multiple_cambia_solicitud', 'Condominio Múltiple cambia solicitud'),
                        ('condom_multiple_cancela_solicitud', 'Condominio Múltiple cancela solicitud'),
                        ('condom_multiple_asigna_descto', 'Condominio Múltiple asigna descto solicitud'),
                        ('condom_multiple_amortizac', 'Condominio Múltiple Listado de amortización'),
                        ('condom_multiple_imprime_amortizac', 'Condominio Múltiple Imprime listado de amortización'),
                        ('condom_multiple_autoriza_visualiza', 'Condominio Múltiple Ver autorizaciones'),
                        ('condom_multiple_autoriza_venta', 'Condominio Múltiple Autoriza solicitud por Gerente ventas'),
                        ('condom_multiple_autoriza_desarrollo', 'Condominio Múltiple Autoriza solicitud por Director desarrollo'),
                        ('condom_multiple_compromiso', 'Condominio Múltiple Realiza compromiso de compra'),
                        ('condom_multiple_pago_compromiso', 'Condominio Múltiple Realizar pago compromiso'),
                        ('condom_multiple_imp_pago_compromiso', 'Condominio Múltiple imprime pago compromiso'),
                        ('condom_multiple_contratar', 'Condominio Múltiple Generar contrato'),
                        ('condom_multiple_datos_contrato', 'Condominio Múltiple Incluir datos al contrato'),
                        ('condom_multiple_imprime_contrato', 'Condominio Múltiple Impresión de contrato'),
                        ('condom_multiple_archivar_contrato', 'Condominio Múltiple Archivar contrato'),
                        ('condom_multiple_consulta_archivo', 'Condominio Múltiple Consultar el histórico de solicitudes'),
                        ('condom_multiple_creditos', 'Condominio Múltiple Consulta contratos a crédito'),
                        ('condom_multiple_contados', 'Condominio Múltiple Consulta contratos de contado'),
            )

    def __str__(self):   
        return '%s, %s, %s' % (self.id, self.lote, self.cliente)

    def _get_titulo_bien(self):
        if self.lote.proyecto.id == 1:
            return 'Contrato %s   %s' % (self.num_contrato, self.lote)
        if self.lote.proyecto.id == 2:
            return 'Contrato %s   %s' % (self.num_contrato, self.lote)
    titulo_bien = property(_get_titulo_bien)

    def _get_total_pagado(self):
        return self.apartado + self.pago_adicional + self.importe_pagado
    total_pagado = property(_get_total_pagado)

    def _get_por_pagar(self):
        return self.precio_final - self.enganche
    por_pagar = property(_get_por_pagar)

    def _get_saldo(self):
        return self.precio_final - self.apartado - self.pago_adicional - self.importe_pagado
    saldo = property(_get_saldo)

    def _get_resta_pagos(self):
        return self.cantidad_pagos - self.pagos_pagados
    resta_pagos = property(_get_resta_pagos)

    def _get_num_contrato(self):
        if self.num_contrato == 0:
            return ""
        return self.num_contrato
    num_contrato_val = property(_get_num_contrato)

    def _get_pagos_vencidos(self):
        meses_vencidos = calcula_vencimiento(self.anio_inicio_pago, self.mes_inicio_pago, self.pagos_pagados)
        return meses_vencidos
    pagos_vencidos = property(_get_pagos_vencidos)

def calcula_vencimiento(par_anio, par_mes, par_pagos_pagados):
#    hoy = datetime.date.now()
#    hoy = datetime.now() 
#    anio = hoy.year
#    mes = hoy.month
    anio = cyear
    mes = cmonth
    if par_mes > mes:   
        mes = mes + 12
        anio = anio - 1
    anio_mes = (anio - par_anio) * 12
    mes_res = mes - par_mes
    meses_debe_pagar = mes_res + anio_mes
    if hoy.day < 10:
        meses_debe_pagar = meses_debe_pagar - 1
    meses_vencidos = meses_debe_pagar - par_pagos_pagados
    if meses_vencidos < 0:
        meses_vencidos = 0
    return meses_vencidos


class Folios(models.Model,PermissionRequiredMixin):
    tipo = models.IntegerField("Tipo folio",choices=TIPO_FOLIO, default=1 )
    numero = models.IntegerField("Número")
    fecha = models.DateTimeField("Fecha de entrega",auto_now_add=True)
    observacion = models.CharField("Observación", max_length=200)
    importe = models.DecimalField("Importe recibo", max_digits=10, decimal_places=2)
    created = models.DateTimeField("Creado", auto_now_add=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='fl_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='fl_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    estatus_folio = models.IntegerField("Estatus",choices=STATUS_FOLIO,default=1)

    class Meta:
        verbose_name = 'Folio'
        verbose_name_plural = 'Folios'
        ordering = ['tipo','numero']
        db_table = 'Folio'

    def __str__(self):   # para poner los nombre en los renglones
        return 'Tipo: %s, Folio: %s, %s, %s' % (self.tipo, self.numero, self.fecha, self.observacion)
