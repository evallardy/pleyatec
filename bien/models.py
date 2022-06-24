from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from empleado.models import *

class Proyecto(models.Model):
    tipo_proyecto = models.IntegerField("Tipo de proyecto",choices=TIPO_PROYECTO,default=1)
    nombre = models.CharField("Nombre proyecto",max_length=60)
    ubicacion = models.CharField("Ubicación",max_length=250)
    estado = models.IntegerField("Estado",choices=ESTADOS, default=0)
    precio_apartir = models.DecimalField('Precio a partir', decimal_places=2, max_digits=10, default=0)
    plano = models.ImageField(upload_to="proyecto", blank=True, null=True)
    estatus_proyecto = models.IntegerField("Activo",choices=STATUS_SI_NO,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='py_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='py_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    app = models.CharField("App",max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['id']
        db_table = 'Proyecto'
        permissions = (('proyecto_nuvole', 'Acceso al proyecto nuvole lotes'),
                       ('proyecto_toscana', 'Acceso al proyecto toscana local comercial'),)

    def __str__(self):   # para poner los nombre en los renglones
        return '%s' % (self.nombre)

    def _get_nombre_completo(self):
        materno = ""
        if not self.materno == None:
            materno = self.materno
        return '%s %s %s' % (self.nombre, self.paterno, materno) 
    nombre_completo = property(_get_nombre_completo)
    
class Lote(models.Model, PermissionRequiredMixin):
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, verbose_name="Proyecto")  
    fase = models.SmallIntegerField("Fase", choices=FASE, default=1, blank=True, null=True)
    manzana = models.SmallIntegerField("Manzana", blank=True, null=True) 
    nivel = models.SmallIntegerField("Nivel", blank=True, null=True) 
    lote = models.CharField("Lote",max_length=10)
    tipo_lote = models.BooleanField("Tipo de lote",choices=TIPO_LOTE, default=1, blank=True, null=True)
    obs_irregular = models.CharField("Medidas",max_length=250, blank=True, null=True)
    fondo = models.DecimalField("Fondo", decimal_places=2, max_digits=10,default=0)
    frente = models.DecimalField("Frente", decimal_places=2, max_digits=10,default=0)
    total = models.DecimalField("Total m²", decimal_places=2, max_digits=10,default=0)
    esquina = models.BooleanField("Esquina",choices=ESQUINA_SI, default=0, blank=True, null=True)
    precio_x_mt = models.DecimalField("Precio por m²", decimal_places=2, max_digits=10, default=0)
    precio = models.DecimalField("Precio", decimal_places=2, max_digits=10, default=0.00)
    colindancia_norte = models.CharField("Colindancia norte",max_length=250, blank=True, null=True)
    colindancia_sur = models.CharField("Colindancia sur",max_length=250, blank=True, null=True)
    colindancia_este = models.CharField("Colindancia este",max_length=250, blank=True, null=True)
    colindancia_oeste = models.CharField("Colindancia oeste",max_length=250, blank=True, null=True)
    terraza = models.DecimalField("Terraza m²", decimal_places=2, max_digits=10, default=0, blank=True, null=True)
    precio_x_mt_t = models.DecimalField("Precio por m² terraza", decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    precio_terraza = models.DecimalField("Precio terraza", decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    gran_total = models.DecimalField("Total gral.", decimal_places=2, max_digits=10, default=0.00, blank=True, null=True)
    altura = models.DecimalField("Altura", decimal_places=2, max_digits=10, default=0, blank=True, null=True)
    estatus_lote = models.IntegerField("Estatus",choices=STATUS_BIEN,default=1)
    asesor = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Asesor", null=True, blank=True)
    coordenadas = models.CharField("Coordenas", max_length=255, blank=True, null=True)
    posicion_x = models.IntegerField("Posición X numero", blank=True, null=True)
    posicion_y = models.IntegerField("Posición Y numero", blank=True, null=True)
    posicion_texto_x = models.IntegerField("Posición X mts", blank=True, null=True)
    posicion_texto_y = models.IntegerField("Posición Y mts", blank=True, null=True)
    posicion_circulo_x = models.IntegerField("Posición X circulo", blank=True, null=True)
    posicion_circulo_y = models.IntegerField("Posición Y circulo", blank=True, null=True)
    estacionamientos = models.IntegerField("Estacionamientos", default=0, blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
 
    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        ordering = ['proyecto','lote']
        unique_together= (('proyecto','fase','manzana','lote'),('proyecto','lote'))
        db_table = 'Lote'
        permissions = (('reservar', 'Reservar bien'),)

    def __str__(self):   # para poner los nombre en los renglones
        if self.proyecto.id == 1:
            return ' Lote: %s Manzana: %s, de la Fase: %s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.id == 2:
            if self.terraza == 0:
                return ' Local: %s nivel: %s' % (self.lote, self.nivel)
            else:
                return ' Local: %s Terraza m²: %s nivel: %s' % (self.lote, self.terraza, self.nivel)
        else:
            return ""

    def _get_colindancia_norte(self):
        colindancia_norte = ""
        if not self.colindancia_norte == None:
            colindancia_norte = self.colindancia_norte
        return '%s' % (self.colindancia_norte) 
    colindancia_norte_val = property(_get_colindancia_norte)

    def _get_combo_bien(self):
        if self.proyecto.id == 1:
            return ' Lote: %s Manzana: %s, de la Fase: %s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.id == 2:
            if self.terraza == 0:
                return ' Local: %s nivel: %s' % (self.lote, self.nivel)
            else:
                return ' Local: %s Terraza: %sm² nivel: %s' % (self.lote, self.terraza, self.nivel)
        else:
            return ""
    combo_bien = property(_get_combo_bien)

    def _get_colindancia_sur(self):
        colindancia_sur = ""
        if not self.colindancia_sur == None:
            colindancia_sur = self.colindancia_sur
        return '%s' % (self.colindancia_sur) 
    colindancia_sur_val = property(_get_colindancia_sur)

    def _get_colindancia_este(self):
        colindancia_este = ""
        if not self.colindancia_este == None:
            colindancia_este = self.colindancia_este
        return '%s' % (self.colindancia_este) 
    colindancia_este_val = property(_get_colindancia_este)

    def _get_colindancia_oeste(self):
        colindancia_oeste = ""
        if not self.colindancia_oeste == None:
            colindancia_oeste = self.colindancia_oeste
        return '%s' % (self.colindancia_oeste) 
    colindancia_oeste_val = property(_get_colindancia_oeste)

class Estacionamiento(models.Model, PermissionRequiredMixin):
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE, verbose_name="Departamento", null=True, blank=True)
    numero = models.CharField("lugar", max_length=10,)
    frente = models.DecimalField("frente", max_digits=2, decimal_places=2, null=True, blank=True)
    fondo = models.DecimalField("fondo", max_digits=2, decimal_places=2, null=True, blank=True)
    total = models.DecimalField("total", max_digits=2, decimal_places=2, null=True, blank=True)
    compartido = models.BooleanField("Compartido", choices=RESP_SI_NO, default=False)
    estatus_estaciona = models.IntegerField("Estatus estacionamiento", choices=STATUS_SI_NO, default=1)
    coordenadas = models.CharField("Coordenas", max_length=255, blank=True, null=True)
    posicion_x = models.IntegerField("Posición X numero", blank=True, null=True)
    posicion_y = models.IntegerField("Posición Y numero", blank=True, null=True)
    posicion_texto_x = models.IntegerField("Posición X mts", blank=True, null=True)
    posicion_texto_y = models.IntegerField("Posición Y mts", blank=True, null=True)
    posicion_circulo_x = models.IntegerField("Posición X circulo", blank=True, null=True)
    posicion_circulo_y = models.IntegerField("Posición Y circulo", blank=True, null=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Estacionamiento'
        verbose_name_plural = 'Estacionamientos'
        ordering = ['lote','numero']
        unique_together= (('lote', 'numero'))
        db_table = 'estacionamiento'

    def __str__(self):   # para poner los nombre en los renglones
        return ' Estacionamiento: %s Departamento: %s' % (self.numero, self.lote)

class Esquema(models.Model, PermissionRequiredMixin):
    nombre_plano = models.CharField("Nombre del plano", max_length=100,)
    esquema = models.ImageField("Plano", upload_to="planos")
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name="PlanoProyecto")
    estatus_plano = models.IntegerField("Estatus plano", choices=STATUS_SI_NO, default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['proyecto','nombre_plano']
        unique_together= (('proyecto', 'nombre_plano'))
        db_table = 'Plano'

    def __str__(self):   # para poner los nombre en los renglones
        return ' Proyecto: %s Plano: %s' % (self.proyecto, self.nombre_plano)

