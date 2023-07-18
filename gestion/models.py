from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.funciones import fecha_hoy
from core.models import *
from cliente.models import *
from bien.models import *
from PIL import Image

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
    precio_lote = models.DecimalField("Precio lote", decimal_places=2, max_digits=10, blank=True, null=True, default=0)
    total = models.DecimalField("Area", decimal_places=2, max_digits=10,default=0)
    precio_x_mt = models.DecimalField("Precio por m²", decimal_places=2, max_digits=10, default=0)
    precio_final = models.DecimalField("Precio final", decimal_places=2, max_digits=10, default=0)
    tipo_descuento = models.IntegerField("Asigna descuento",choices=TIPO_DESCUENTO, default=1)
    porcentaje_descuento = models.DecimalField("Porcentaje desc.", decimal_places=2, max_digits=4, default=0)
    descuento = models.DecimalField("Descuento", decimal_places=2, max_digits=10, default=0)
    modo_pago = models.IntegerField("Modo de pago",choices=MODO_PAGO,default=1)
    enganche = models.DecimalField("Enganche", decimal_places=2, max_digits=10, default=0)
#  Pago apartado
    apartado = models.DecimalField("Apartado", decimal_places=2, max_digits=10, default=0)
    confirmacion_apartado = models.IntegerField("Depósito apartado", choices=STATUS_DEPOSITO, default=0)
    foto_comprobante_apartado = models.FileField('Comprobante cliente apartado', upload_to="compApartado", blank=True, null=True)
    forma_pago_apa = models.IntegerField("Forma pago apartado",choices=STATUS_FORMA_PAGO, default=0)
    cuenta_apa = models.CharField("Número de cuenta apartado",max_length=4, blank=True, null=True)
    numero_comprobante_apa = models.CharField("Número de comprobante apartado",max_length=40, blank=True, null=True)
    recibo_firmado_apa = models.FileField('Recibo firmado apartado', upload_to="compApartado/firmado", blank=True, null=True)
#  Pago adicional
    pago_adicional = models.DecimalField("Pago adicional", decimal_places=2, max_digits=10, default=0)
    confirmacion_pago_adicional = models.IntegerField("Depósito PA", choices=STATUS_DEPOSITO, default=0)
    foto_comprobante_pago_adicional = models.FileField('Comprobante cliente pago adicional', upload_to="compAdicional", blank=True, null=True)
    forma_pago_pa = models.IntegerField("Forma pago pago adic.",choices=STATUS_FORMA_PAGO, default=0)
    cuenta_pa = models.CharField("Número de cuenta pago adic",max_length=4, blank=True, null=True)
    numero_comprobante_pa = models.CharField("Número de comprobante pago adic",max_length=40, blank=True, null=True)
    fecha_confirma_pago_adicional = models.DateField("Fecha confirmado", blank=True, null=True)
    recibo_firmado_pa = models.FileField('Recibo firmado pago adic', upload_to="compAdicional/firmado", blank=True, null=True)

    cantidad_pagos = models.IntegerField("Pagos", default=0)
    importe_x_pago = models.DecimalField("Importe por pago", decimal_places=2, max_digits=10, default=0)
    credito = models.DecimalField("Crédito", decimal_places=2, max_digits=10, default=0)
    aprobacion_gerente = models.SmallIntegerField("Aprobación gerente de ventas", choices=RESP_SI_NO, default=0)
    aprobacion_director = models.SmallIntegerField("Aprobación director desarrollo", choices=RESP_SI_NO, default=0)
    foto_elector_frente = models.FileField(upload_to="ine", blank=True, null=True)
    foto_elector_reverso = models.FileField(upload_to="ine", blank=True, null=True)
    foto_elector_frente_cy = models.FileField(upload_to="ine_cy", blank=True, null=True)
    foto_elector_reverso_cy = models.FileField(upload_to="ine_cy", blank=True, null=True)
    foto_matrimonio = models.FileField(upload_to="matrimonio", blank=True, null=True)
    foto_comprobante = models.FileField(upload_to="comprobante", blank=True, null=True)
    foto_alta_shcp = models.FileField(upload_to="alta_shcp", blank=True, null=True)
    foto_acta_const = models.FileField(upload_to="acte_const", blank=True, null=True)
    num_apartado = models.IntegerField("Recibo apartado", default=0)
    num_adicional = models.IntegerField("Recibo adicional", default=0)
    num_contrato = models.IntegerField("Número de contrato", default=0)
    pagos_pagados = models.IntegerField("Pagos realizados", default=0)
    importe_pagado = models.DecimalField("Importe pagado", decimal_places=2, max_digits=10, default=0)
    asigna_descuento = models.SmallIntegerField("Asigna descuento",choices=RESP_SI_NO, default=0)
    porcentaje_descuento = models.DecimalField("Descuento", decimal_places=2, max_digits=5, default=0)
    fecha_contrato = models.DateField("Fecha de contrato", blank=True, null=True)
    mes_inicio_pago = models.DecimalField("Mes de inicio de pago", choices=MESES, decimal_places=0, max_digits=2, default=0)
    anio_inicio_pago = models.DecimalField("Año de inicio de pago", choices=ANIOS, decimal_places=0, max_digits=4, default=0)
    estatus_solicitud = models.IntegerField("Estatus",choices=STATUS_SOLICITUD, default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='sl_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='sl_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    tipo_cliente = models.SmallIntegerField("Tipo de cliente", choices=TIPO_CLIENTE, default=0)
    razon = models.CharField("Razón social",max_length=255, blank=True, null=True)
    nombre = models.CharField("Nombre",max_length=30, blank=True, null=True)
    paterno = models.CharField("Paterno",max_length=30, blank=True, null=True)
    materno = models.CharField("Materno",max_length=30, blank=True, null=True)
    nombre_conyuge = models.CharField("Nombre coyugue",max_length=30, blank=True, null=True)
    paterno_conyuge = models.CharField("Paterno coyugue",max_length=30, blank=True, null=True)
    materno_conyuge = models.CharField("Materno coyugue",max_length=30, blank=True, null=True)
    rfc = models.CharField("R.F.C.",max_length=20, blank=True, null=True)
    curp = models.CharField("CURP",max_length=18, blank=True, null=True)
    estado_civil = models.SmallIntegerField("Estado civil", choices=ESTADO_CIVIL, default=1)
    regimen = models.IntegerField("Régime", choices=REGIMEN, default=0)
    calle = models.CharField("Calle y núm.",max_length=250, blank=True, null=True)
    colonia = models.CharField("Colonia",max_length=200, blank=True, null=True)
    codpos = models.CharField("Código Postal",max_length=5, blank=True, null=True)
    municipio = models.CharField("Municipio",max_length=150, blank=True, null=True)
    estado = models.SmallIntegerField("Estado",choices=ESTADOS, default=0)
    celular = models.CharField("Celular", max_length=20, blank=True, null=True)
    correo = models.CharField("Correo", max_length=180, blank=True, null=True)
    comision_pagada = models.SmallIntegerField("Comision pagada", choices=RESP_SI_NO, default=0)

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
                        ('nuvole_autoriza_desarrollo', 'Nuvole Autoriza solicitud por Director Desarrollo'),
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
                        ('toscana_autoriza_desarrollo', 'Toscana Autoriza solicitud por Director Desarrollo'),
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
                        ('local_punta_o_autoriza_desarrollo', 'Local Punta O Autoriza solicitud por Director Desarrollo'),
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
                        ('consul_punta_o_autoriza_desarrollo', 'Consultorio Punta O Autoriza solicitud por Director Desarrollo'),
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
                        ('torre_vento_autoriza_desarrollo', 'Torre Vento Autoriza solicitud por Director Desarrollo'),
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
            #  Porto Santo
                        ('porto_santo_ver_solicitud', 'Porto Santo Listado ver solicitudes'),
                        ('porto_santo_add_solicitud', 'Porto Santo agrega solicitud'),
                        ('porto_santo_cambia_solicitud', 'Porto Santo cambia solicitud'),
                        ('porto_santo_cancela_solicitud', 'Porto Santo cancela solicitud'),
                        ('porto_santo_asigna_descto', 'Porto Santo asigna descto solicitud'),
                        ('porto_santo_amortizac', 'Porto Santo Listado de amortización'),
                        ('porto_santo_imprime_amortizac', 'Porto Santo Imprime listado de amortización'),
                        ('porto_santo_autoriza_visualiza', 'Porto Santo Ver autorizaciones'),
                        ('porto_santo_autoriza_venta', 'Porto Santo Autoriza solicitud por Gerente ventas'),
                        ('porto_santo_autoriza_desarrollo', 'Porto Santo Autoriza solicitud por Director Desarrollo'),
                        ('porto_santo_compromiso', 'Porto Santo Realiza compromiso de compra'),
                        ('porto_santo_pago_compromiso', 'Porto Santo Realizar pago compromiso'),
                        ('porto_santo_imp_pago_compromiso', 'Porto Santo imprime pago compromiso'),
                        ('porto_santo_contratar', 'Porto Santo Generar contrato'),
                        ('porto_santo_datos_contrato', 'Porto Santo Incluir datos al contrato'),
                        ('porto_santo_imprime_contrato', 'Porto Santo Impresión de contrato'),
                        ('porto_santo_archivar_contrato', 'Porto Santo Archivar contrato'),
                        ('porto_santo_consulta_archivo', 'Porto Santo Consultar el histórico de solicitudes'),
                        ('porto_santo_creditos', 'Porto Santo Consulta contratos a crédito'),
                        ('porto_santo_contados', 'Porto Santo Consulta contratos de contado'),
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
                        ('vivienda_nuvole_autoriza_desarrollo', 'Vivienda Nuvole Autoriza solicitud por Director Desarrollo'),
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
            #  Monte Cristallo
                        ('monte_cristallo_ver_solicitud', 'Monte cristallo Listado ver solicitudes'),
                        ('monte_cristallo_add_solicitud', 'Monte cristallo agrega solicitud'),
                        ('monte_cristallo_cambia_solicitud', 'Monte cristallo cambia solicitud'),
                        ('monte_cristallo_cancela_solicitud', 'Monte cristallo cancela solicitud'),
                        ('monte_cristallo_asigna_descto', 'Monte cristallo asigna descto solicitud'),
                        ('monte_cristallo_amortizac', 'Monte cristallo Listado de amortización'),
                        ('monte_cristallo_imprime_amortizac', 'Monte cristallo Imprime listado de amortización'),
                        ('monte_cristallo_autoriza_visualiza', 'Monte cristallo Ver autorizaciones'),
                        ('monte_cristallo_autoriza_venta', 'Monte cristallo Autoriza solicitud por Gerente ventas'),
                        ('monte_cristallo_autoriza_desarrollo', 'Monte cristallo Autoriza solicitud por Director Desarrollo'),
                        ('monte_cristallo_compromiso', 'Monte cristallo Realiza compromiso de compra'),
                        ('monte_cristallo_pago_compromiso', 'Monte cristallo Realizar pago compromiso'),
                        ('monte_cristallo_imp_pago_compromiso', 'Monte cristallo imprime pago compromiso'),
                        ('monte_cristallo_contratar', 'Monte cristallo Generar contrato'),
                        ('monte_cristallo_datos_contrato', 'Monte cristallo Incluir datos al contrato'),
                        ('monte_cristallo_imprime_contrato', 'Monte cristallo Impresión de contrato'),
                        ('monte_cristallo_archivar_contrato', 'Monte cristallo Archivar contrato'),
                        ('monte_cristallo_consulta_archivo', 'Monte cristallo Consultar el histórico de solicitudes'),
                        ('monte_cristallo_creditos', 'Monte cristallo Consulta contratos a crédito'),
                        ('monte_cristallo_contados', 'Monte cristallo Consulta contratos de contado'),
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
                        ('condom_multiple_autoriza_desarrollo', 'Condominio Múltiple Autoriza solicitud por Director Desarrollo'),
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
            # Nuvole 2
                        ('nuvole2_ver_solicitud', 'Nuvole 2 Listado ver solicitudes'),
                        ('nuvole2_add_solicitud', 'Nuvole 2 agrega solicitud'),
                        ('nuvole2_cambia_solicitud', 'Nuvole 2 cambia solicitud'),
                        ('nuvole2_cancela_solicitud', 'Nuvole 2 cancela solicitud'),
                        ('nuvole2_asigna_descto', 'Nuvole 2 asigna descto solicitud'),
                        ('nuvole2_amortizac', 'Nuvole 2 Listado de amortización'),
                        ('nuvole2_imprime_amortizac', 'Nuvole 2 Imprime listado de amortización'),
                        ('nuvole2_autoriza_visualiza', 'Nuvole 2 Ver autorizaciones'),
                        ('nuvole2_autoriza_venta', 'Nuvole 2 Autoriza solicitud por Gerente ventas'),
                        ('nuvole2_autoriza_desarrollo', 'Nuvole 2 Autoriza solicitud por Director Desarrollo'),
                        ('nuvole2_compromiso', 'Nuvole 2 Realiza compromiso de compra'),
                        ('nuvole2_pago_compromiso', 'Nuvole 2 Realizar pago compromiso'),
                        ('nuvole2_imp_pago_compromiso', 'Nuvole 2 imprime pago compromiso'),
                        ('nuvole2_contratar', 'Nuvole 2 Generar contrato'),
                        ('nuvole2_datos_contrato', 'Nuvole 2 Incluir datos al contrato'),
                        ('nuvole2_imprime_contrato', 'Nuvole 2 Impresión de contrato'),
                        ('nuvole2_archivar_contrato', 'Nuvole 2 Archivar contrato'),
                        ('nuvole2_consulta_archivo', 'Nuvole 2 Consultar el histórico de solicitudes'),
                        ('nuvole2_creditos', 'Nuvole 2 Consulta contratos a crédito'),
                        ('nuvole2_contados', 'Nuvole 2 Consulta contratos de contado'),
            )

    def __str__(self):   
        return '%s, %s, %s' % (self.id, self.lote, self.cliente)

    def _get_nombre_completo(self):
        if not self.nombre:
            var_nombre = " "
        else:
            var_nombre = self.nombre
        if not self.paterno:
            var_paterno = " "
        else:
            var_paterno = self.paterno
        if not self.materno:
            var_materno = " "
        else:
            var_materno = self.materno
        nombre_completo = var_nombre + " " + var_paterno + " " + var_materno
        return nombre_completo
    nombre_completo = property(_get_nombre_completo)

    def _get_descripcion_cliente(self):
        if self.tipo_cliente == 0:
            if not self.nombre:
                var_nombre = " "
            else:
                var_nombre = self.nombre
            if not self.paterno:
                var_paterno = " "
            else:
                var_paterno = self.paterno
            if not self.materno:
                var_materno = " "
            else:
                var_materno = self.materno
            nombre_completo = var_nombre + " " + var_paterno + " " + var_materno
        else:
            nombre_completo = self.razon
        return nombre_completo
    descripcion_cliente = property(_get_descripcion_cliente)

    def _get_cliente_inicio_contrato(self):
        if not self.nombre:
            var_nombre = " "
        else:
            var_nombre = self.nombre
        if not self.paterno:
            var_paterno = " "
        else:
            var_paterno = self.paterno
        if not self.materno:
            var_materno = " "
        else:
            var_materno = self.materno
        nombre_completo = var_nombre + " " + var_paterno + " " + var_materno
        representante = ""
        if self.tipo_cliente == 1:
            representante = self.razon + " a través de su apoderado legal " + nombre_completo
        else:
            representante = nombre_completo
        return representante
    cliente_inicio_contrato = property(_get_cliente_inicio_contrato)

    def _get_representante(self):
        representante = ""
        if self.tipo_cliente == 1:
            representante = "Apoderado legal"
        return representante
    representante = property(_get_representante)

    def _get_titulo_bien(self):
        if self.lote.proyecto.id == 1:
            return 'Contrato %s   %s' % (self.num_contrato, self.lote)
        if self.lote.proyecto.id == 2:
            return 'Contrato %s   %s' % (self.num_contrato, self.lote)
    titulo_bien = property(_get_titulo_bien)

    def _get_entrega(self):
        if self.lote.fase == 1:
            return "30 de abril 2022"
        elif self.lote.fase == 2:
            return "30 de junio 2022"
        elif self.lote.fase == 3:
            return "31 de julio 2022"
        else:
            return ""
    entrega = property(_get_entrega)

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
    observacion = models.CharField("Observación", max_length=200, default=" ")
    importe = models.DecimalField("Importe recibo", max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    estatus_folio = models.IntegerField("Estatus",choices=STATUS_FOLIO,default=1)

    class Meta:
        verbose_name = 'Folio'
        verbose_name_plural = 'Folios'
        ordering = ['tipo','numero']
        db_table = 'Folio'

    def __str__(self):   # para poner los nombre en los renglones
        return 'Tipo: %s, Folio: %s, %s, %s' % (self.tipo, self.numero, self.fecha, self.observacion)

class Regla(models.Model,PermissionRequiredMixin):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name="Proyecto")
    modo_pago = models.IntegerField("Modo de pago",choices=MODO_PAGO,default=1)
    tipo_aplica_descto = models.IntegerField("Tipo aplicación descto.",choices=TIPO_APLICA_DESCUENTO, default=0)
    valor1 = models.DecimalField("Valor descto. bien", decimal_places=7, max_digits=17, default=0)
    valor11 = models.DecimalField("Valor descto. terraza", decimal_places=2, max_digits=10, default=0)
    tipo_apartado_minimo = models.IntegerField("Tipo apartado mínimo",choices=TIPO_APARTADO_MINIMO, default=0)
    valor2 = models.DecimalField("Valor apartado", decimal_places=2, max_digits=10, default=0)
    tipo_enganche_minimo = models.IntegerField("Tipo enganche mínimo",choices=TIPO_ENGANCHE_MINIMO, default=0)
    valor3 = models.DecimalField("Valor enganche", decimal_places=2, max_digits=10, default=0)
    mensualidades_permitidas = models.IntegerField("Mensualidades permitidas", default=0)

    class Meta:
        verbose_name = 'Regla' 
        verbose_name_plural = 'Reglas' 
        ordering = ['proyecto','modo_pago','mensualidades_permitidas']
        unique_together= (('proyecto','modo_pago','valor1','mensualidades_permitidas'))
        db_table = 'Regla'

    def __str__(self):
        return 'Proyecto: %s, Modo de pago: %s, Mensualidades: %s' % (self.proyecto, self.modo_pago, self.mensualidades_permitidas)
