from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from numpy import False_
from core.models import *
from empleado.models import *

class Cliente(models.Model, PermissionRequiredMixin):
    tipo_cliente = models.IntegerField("Tipo de cliente", choices=TIPO_CLIENTE, default=0)
    razon = models.CharField("Razón social",max_length=255, blank=True, null=True)
    nombre = models.CharField("Nombre",max_length=30, blank=True, null=True)
    paterno = models.CharField("Paterno",max_length=30, blank=True, null=True)
    materno = models.CharField("Materno",max_length=30, blank=True, null=True)
    nombre_conyuge = models.CharField("Nombre coyugue", max_length=30, blank=True, null=True)
    paterno_conyuge = models.CharField("Paterno coyugue", max_length=30, blank=True, null=True)
    materno_conyuge = models.CharField("Materno coyugue", max_length=30, blank=True, null=True)
    rfc = models.CharField("R.F.C.",max_length=20, blank=True, null=True)
    curp = models.CharField("CURP",max_length=18, blank=True, null=True)
    fecha_nac = models.DateField("Fecha de nacimiento", null=True, blank=True)
    genero = models.CharField("Género", max_length=1, choices=GENERO, default='M')
    estado_civil = models.SmallIntegerField("Estado civil", choices=ESTADO_CIVIL, default=1)
    regimen = models.SmallIntegerField("Régime", choices=REGIMEN, default=0)
    calle = models.CharField("Calle y núm.",max_length=250, blank=True, null=True)
    colonia = models.CharField("Colonia",max_length=200, blank=True, null=True)
    codpos = models.CharField("Código Postal",max_length=5, blank=True, null=True)
    municipio = models.CharField("Municipio",max_length=150, blank=True, null=True)
    estado = models.SmallIntegerField("Estado",choices=ESTADOS, default=0)
    celular = models.CharField("Celular", max_length=20, blank=True, null=True)
    correo = models.EmailField("Correo", max_length=180, blank=True, null=True)
    estatus_cliente = models.SmallIntegerField("Activo",choices=STATUS_SI_NO,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    asesor = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='ct_user_asesor',
         verbose_name="Asesor", null=True, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['paterno','materno','nombre']
#        unique_together= (('rfc',),('curp',),)
        db_table = 'Cliente'

    def __str__(self):   # para poner los nombre en los renglones
        if self.tipo_cliente == 0:
            if self.nombre == None:
                nombre = ""
            else:
                nombre = self.nombre
            if self.materno == None:
                materno = ""
            else:
                materno = self.materno
            if self.paterno == None:
                paterno = ""
            else:
                paterno = self.paterno
            razon = nombre + " " + paterno + " " + materno
        else:
            razon = self.razon
        return '%s' % (razon) 
    
    def _get_nombre_completo(self):
        if self.nombre == None:
            nombre = ""
        else:
            nombre = self.nombre
        if self.materno == None:
            materno = ""
        else:
            materno = self.materno
        if self.paterno == None:
            paterno = ""
        else:
            paterno = self.paterno
#        if self.tipo_cliente == 0:
        razon = nombre + " " + paterno + " " + materno
#        else:
#            razon = self.razon
        return '%s' % (razon) 
    nombre_completo = property(_get_nombre_completo)

    def _get_cliente_nombre(self):
        if self.tipo_cliente == 0:
            if self.materno == None:
                materno = ""
            else:
                materno = self.materno
            if self.paterno == None:
                paterno = ""
            else:
                paterno = self.paterno
            razon = self.nombre + " " + paterno + " " + materno
        else:
            razon = self.razon
        return '%s' % (razon) 
    cliente_nombre = property(_get_cliente_nombre)

    def _get_rfc(self):
        rfc = ""
        if not self.rfc == None:
            rfc = self.rfc
        return '%s' % (rfc)
    rfc_val = property(_get_rfc)

    def _get_razon_null(self):
        razon = ""
        if not self.razon == None:
            razon = self.razon
        return '%s' % (razon)
    razon_null = property(_get_razon_null)

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

