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
    cuenta = models.CharField("Número de cuenta",max_length=25, null=True, blank=True, default="")
    numero_comprobante = models.CharField("Número de comprobante",max_length=40, null=True, blank=True, default="")
    estatus_pago = models.IntegerField("Estatus de pago",choices=STATUS_PAGO,default=1)
    foto_voucher = models.ImageField(upload_to="vouchers", blank=True, null=True,default=" ")
    created = models.DateTimeField("Creado", auto_now_add=True, null=True, blank=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='pg_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True, null=True, blank=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='pg_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['convenio', 'numero_pago'], name="%(app_label)s_%(class)s_unique")
        ]

    class Meta:
        verbose_name = 'Pagos'
        verbose_name_plural = 'Pago'
        ordering = ['id']
        db_table = 'Pago'
        permissions = (('estado_cuenta', 'Mostrar estado de cuenta'),
                    ('listado_pagos', 'Mostrar listado de pagos'),
                    ('comprobante_pagos', 'Incluir comprobante de pago'),)

    def __str__(self):   
        return '%s, %s, %s, %s, %s, fecha_voucher:%s' % (self.id, self.convenio, self.numero_pago, self.fecha_pago, self.fecha_pago, self.fecha_voucher)

