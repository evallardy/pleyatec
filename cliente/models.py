from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from empleado.models import *

class Cliente(models.Model, PermissionRequiredMixin):
    nombre = models.CharField("Nombre",max_length=30)
    paterno = models.CharField("Paterno",max_length=30, null=True, blank=True, default=" ")
    materno = models.CharField("Materno",max_length=30, null=True, blank=True, default=" ")
    nombre_conyuge = models.CharField("Nombre coyugue",max_length=30, null=True, blank=True)
    paterno_conyuge = models.CharField("Paterno coyugue",max_length=30, null=True, blank=True)
    materno_conyuge = models.CharField("Materno coyugue",max_length=30, null=True, blank=True)
    rfc = models.CharField("R.F.C.",max_length=20, blank=True, null=True)
    curp = models.CharField("CURP",max_length=18, null=True, blank=True)
    fecha_nac = models.DateField("Fecha de nacimiento", null=True, blank=True)
    genero = models.CharField("Género", max_length=1, choices=GENERO, null=True, blank=True)
    estado_civil = models.SmallIntegerField("Estado civil", choices=ESTADO_CIVIL, null=True, blank=True)
    calle = models.CharField("Calle y núm.",max_length=250, blank=True, null=True)
    colonia = models.CharField("Colonia",max_length=200, blank=True, null=True)
    codpos = models.CharField("Código Postal",max_length=5, blank=True, null=True)
    municipio = models.CharField("Municipio",max_length=150, blank=True, null=True)
    estado = models.SmallIntegerField("Estado",choices=ESTADOS, blank=True, null=True, default=0)
    telefono_fijo = models.CharField("Telefono fijo", max_length=50, blank=True, null=True)
    celular = models.CharField("Celular", max_length=10, blank=True, null=True)
    correo = models.EmailField("Correo", max_length=180, blank=True, null=True)
    estatus_cliente = models.SmallIntegerField("Activo",choices=STATUS_SI_NO,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ct_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ct_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    asesor = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ct_user_asesor',
         verbose_name="Asesor", null=True, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['paterno','materno','nombre']
        unique_together= (('rfc',),('curp',),)
        db_table = 'Cliente'

    def __str__(self):   # para poner los nombre en los renglones
        if self.materno == None:
            materno = ""
        else:
            materno = self.materno
        return '%s %s %s' % (self.nombre, self.paterno, materno) 
    
    def _get_nombre_completo(self):
        materno = ""
        if not self.materno == None:
            materno = self.materno
        return '%s %s %s' % (self.nombre, self.paterno, materno) 
    nombre_completo = property(_get_nombre_completo)

    def _get_rfc(self):
        rfc = ""
        if not self.rfc == None:
            rfc = self.rfc
        return '%s' % (rfc)
    rfc_val = property(_get_rfc)

    def _get_telefono_fijo(self):
        telefono_fijo = ""
        if not self.telefono_fijo == None:
            telefono_fijo = self.telefono_fijo
        return '%s' % (telefono_fijo)
    telefono_fijo_val = property(_get_telefono_fijo)

    def _get_celular(self):
        celular = ""
        if not self.celular == None:
            celular = self.celular
        return '%s' % (celular)
    celular_val = property(_get_celular)

    def _get_correo(self):
        correo = ""
        if not self.correo == None:
            correo = self.correo
        return '%s' % (correo)
    correo_val = property(_get_correo)

    def _get_asesor_id(self):
        asesor_id = ""
        if not self.asesor_id == None:
            asesor_id = self.asesor_id
        return '%s' % (asesor_id)
    asesor_id_val = property(_get_asesor_id)

