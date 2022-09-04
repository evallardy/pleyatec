from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from django.contrib.auth.models import User

class Empleado(models.Model,PermissionRequiredMixin):
    nombre = models.CharField("Nombre",max_length=30)
    paterno = models.CharField("Paterno",max_length=30)
    materno = models.CharField("Materno",max_length=30, default=" ")
    # Relacion recursiva, poniendo el nombre del Proveedor en la relacion
    subidPersdonal = models.ForeignKey('self',null=True, on_delete=models.SET_NULL, blank=True, related_name='Personal',verbose_name="Asignado a") 
    rfc = models.CharField("R.F.C.",max_length=20, default=" ")
    curp = models.CharField("CURP",max_length=18, default=" ")
    fecha_nac = models.DateField("Fecha de nacimiento", null=True, blank=True)
    genero = models.CharField("Género", max_length=1, choices=GENERO_P, default='M')
    estado_civil = models.IntegerField("Estado civil", choices=ESTADO_CIVIL, default=1)
    numero_seguro_social = models.CharField("Número de seguro social", max_length=12, default=" ")
    cuenta_banco = models.CharField("Cuenta nómina", max_length=18, default=" ")
    banco = models.ForeignKey('core.Banco', on_delete=models.CASCADE, verbose_name="Banco cta. depositar", null=True, blank=True)
    tipo_pago = models.CharField("Pago",max_length=1,choices=PAGO,default='Q')
#    id_tabulador = models.ForeignKey("Tabulador", on_delete=models.SET_NULL, blank=True, null=True,verbose_name="Tabulador")
    calle_num = models.CharField("Dirección",max_length=250, default=" ")
    colonia = models.CharField("Colonia",max_length=200, default=" ")
    municipio = models.CharField("Municipio",max_length=150, default=" ")
    estado = models.IntegerField("Estado",choices=ESTADOS, default=0)
    codpos = models.CharField("Código Postal",max_length=5, default=" ")
    telefono_fijo = models.CharField("Telefono fijo", max_length=50, default=" ")
    celular = models.CharField("Celular", max_length=20, default=" ")
    correo = models.EmailField("Correo", max_length=180, blank=True, null=True)
    tipo_empleado = models.CharField("Interno/Externo", max_length=1, choices=TIPO_EMPLEADO,default='E')
    area_operativa = models.SmallIntegerField("Área operativa", choices=AREA_OPERATIVA,default=3)
    puesto = models.SmallIntegerField("Puesto", choices=PUESTO,default=1)
    asigna_solicitud = models.SmallIntegerField("Asigna solicitudes",choices=RESP_SI_NO, default=0)
    estatus_empleado = models.IntegerField("Estatus",choices=STATUS_SI_NO,default=1)
    foto = models.ImageField(upload_to="personal", blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='em_auth_user',
        verbose_name="Usuario", null=True, blank=True)

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Personal'
        ordering = ['paterno','materno','nombre']
        db_table = 'Empleado'
        permissions = (
                ('comisiones_asesor', 'Comisiones por asesor'),
        )


    def _get_materno(self):
        materno = ""
        if not self.materno == None:
            materno = self.materno
        return '%s' % (materno)
    materno_val = property(_get_materno)

    def __str__(self):   # para poner los nombre en los renglones
        return '%s %s, %s' % (self.paterno, self.materno_val, self.nombre)

    def _get_nombre_completo(self):
        return '%s %s %s' % (self.nombre, self.paterno, self.materno_val) 
    nombre_completo = property(_get_nombre_completo)

    def _get_rfc(self):
        rfc = ""
        if not self.rfc == None:
            rfc = self.rfc
        return '%s' % (rfc)
    rfc_val = property(_get_rfc)

    def _get_curp(self):
        curp = ""
        if not self.curp == None:
            curp = self.curp
        return '%s' % (curp)
    curp_val = property(_get_curp)

    def _get_fecha_nac(self):
        fecha_nac = ""
        if not self.fecha_nac == None:
            fecha_nac = self.fecha_nac
        return '%s' % (fecha_nac)
    fecha_nac_val = property(_get_fecha_nac)
    
    def _get_estado_civil(self):
        estado_civil = ""
        if not self.estado_civil == None:
            estado_civil = self.estado_civil
        return '%s' % (estado_civil)
    estado_civil_val = property(_get_estado_civil)

    def _get_numero_seguro_social(self):
        numero_seguro_social = ""
        if not self.numero_seguro_social == None:
            numero_seguro_social = self.numero_seguro_social
        return '%s' % (numero_seguro_social)
    numero_seguro_social_val = property(_get_numero_seguro_social)

    def _get_cuenta_banco(self):
        cuenta_banco = ""
        if not self.cuenta_banco == None:
            cuenta_banco = self.cuenta_banco
        return '%s' % (cuenta_banco)
    cuenta_banco_val = property(_get_cuenta_banco)

    def _get_banco(self):
        banco = ""
        if not self.banco == None:
            banco = self.banco
        return '%s' % (banco)
    banco_val = property(_get_banco)

    def _get_calle_num(self):
        calle_num = ""
        if not self.calle_num == None:
            calle_num = self.calle_num
        return '%s' % (calle_num)
    calle_num_val = property(_get_calle_num)

    def _get_colonia(self):
        colonia = ""
        if not self.colonia == None:
            colonia = self.colonia
        return '%s' % (colonia)
    colonia_val = property(_get_colonia)

    def _get_municipio(self):
        municipio = ""
        if not self.municipio == None:
            municipio = self.municipio
        return '%s' % (municipio)
    municipio_val = property(_get_municipio)

    def _get_estado(self):
        estado = ""
        if not self.estado == None:
            estado = self.estado
        return '%s' % (estado)
    estado_val = property(_get_estado)

    def _get_codpos(self):
        codpos = ""
        if not self.codpos == None:
            codpos = self.codpos
        return '%s' % (codpos)
    codpos_val = property(_get_codpos)

    def _get_estado_civil(self):
        estado_civil = ""
        if not self.estado_civil == None:
            estado_civil = self.estado_civil
        return '%s' % (estado_civil)
    estado_civil_val = property(_get_estado_civil)

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

    def _get_subidPersdonal(self):
        subidPersdonal = ""
        if self.subidPersdonal_id == None:
            return '%s' % (subidPersdonal)
        else:
            return self.subidPersdonal.nombre_completo
    subidPersdonal_val = property(_get_subidPersdonal)

