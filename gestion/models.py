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
    apartado = models.DecimalField("Apartado", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    cantidad_pagos = models.IntegerField("Pagos", null=True, blank=True, default=0)
    importe_x_pago = models.DecimalField("Importe por pago", decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    aprobacion_gerente = models.BooleanField("Aprobación gerente de ventas", default=False)
    aprobacion_director = models.BooleanField("Aprobación director desarrollo", default=False)
    foto_elector_frente = models.ImageField(upload_to="documentos", blank=True, null=True,default=" ")
    foto_elector_reverso = models.ImageField(upload_to="documentos", blank=True, null=True,default=" ")
    foto_matrimonio = models.ImageField(upload_to="documentos", blank=True, null=True,default=" ")
    foto_comprobante = models.ImageField(upload_to="documentos", blank=True, null=True,default=" ")
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

    class Meta:
        verbose_name = 'Solicitud' 
        verbose_name_plural = 'Solicitudes' 
        ordering = ['id']
        db_table = 'Solicitud'
        permissions = (('autoriza_visualiza', 'Ver autorizaciones'),
                        ('autoriza_venta', 'Autoriza solicitud por Gerente ventas'),
                        ('autoriza_desarrollo', 'Autoriza solicitud por Director desarrollo'),
                        ('consulta_archivo', 'Consultar el histórico de solicitudes'),
                        ('compromiso', 'Realiza compromiso de compra'),
                        ('creditos', 'Consulta contratos a crédito'),
                        ('contados', 'Consulta contratos de contado'),
                        ('check_pagos', 'Check list de pagos'),
                        ('pago_compromiso', 'Realizar pago compromiso'),
                        ('contratar', 'Generar contrato'),
                        ('datos_contrato', 'Incluir datos al contrato'),
                        ('imprime_contrato', 'Impresión de contrato'),
                        ('archivar_contrato', 'Archivar contrato'),
                        ('amortizacion', 'Listado de amortización'),
                        ('imprime_amortizacion', 'Imprime listado de amortización'),)
        

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
