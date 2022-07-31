from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from empleado.models import Empleado

class Proyecto(models.Model):
    tipo_proyecto = models.IntegerField("Tipo de proyecto",choices=TIPO_PROYECTO,default=1)
    singular = models.CharField("Proyecto en sigular",max_length=50, blank=True, null=True)
    nombre = models.CharField("Nombre proyecto",max_length=60)
    ubicacion = models.CharField("Ubicación",max_length=250)
    estado = models.IntegerField("Estado",choices=ESTADOS, default=0)
    precio_apartir = models.DecimalField('Precio a partir', decimal_places=2, max_digits=10, default=0)
    plano = models.ImageField(upload_to="proyecto", blank=True, null=True)
    estatus_proyecto = models.IntegerField("Activo",choices=STATUS_SI_NO,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    comision_asesor = models.DecimalField("Comision Asesor", max_digits=4, decimal_places=2, default=0)
    comision_jefe_asesor = models.DecimalField("Comision jefe Asesor", max_digits=4, decimal_places=2, default=0)
    usuario_ins = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='py_user_ins',
        verbose_name="Usuario insertó", null=True, blank=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    usuario_mod = models.ForeignKey(Empleado, on_delete=models.SET_NULL, related_name='py_user_mod',
        verbose_name="Usuario modificó", null=True, blank=True)
    app = models.CharField("App",max_length=20, blank=True, null=True)
    nom_proy = models.CharField("Abrev Proyecto",max_length=30, blank=True, null=True, default=" ")

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['id']
        db_table = 'Proyecto'
        permissions = (
                       ('nuvole_acceso', 'Nuvole Acceso'),
                       ('toscana_acceso', 'Toscana Acceso'),
                       ('local_punta_o_acceso', 'Local Punta O Acceso'),
                       ('consul_punta_o_acceso', 'Consultorio Punta O Acceso'),
                       ('torre_vento_acceso', 'Torre Vento Acceso'),
                       ('fraccion34_acceso', 'Fracción 34 Acceso'),
                       ('vivienda_nuvole_acceso', 'Vivienda Nuvole Acceso'),
                       ('pathe_acceso', 'Pathe Acceso'),
                       ('condom_multiple_acceso', 'Condominio Múltiple Acceso'),
                       ('comision_proyectos', 'Comisiones por proyecto'),
                       )

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
    bien_anexo = models.CharField('Anexo del bien', max_length=12, null=True, blank=True)
    gpo_lote = models.CharField('Grupo de bienes', max_length=12, null=True, blank=True)
    reciente = models.IntegerField('Ultimos lotes', default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    comision_pagada = models.IntegerField("Comision pagada", choices=RESP_SI_NO, default=0)
 
    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        ordering = ['proyecto','lote']
        unique_together= (('proyecto','fase','manzana','lote'),('proyecto','lote'))
        db_table = 'Lote'
        permissions = (
            #  Nuvole
                       ('nuvole_ver', 'Nuvole ver bienes'),
                       ('nuvole_add', 'Nuvole agregar bien'),
                       ('nuvole_chag', 'Nuvole cambiar bien'),
                       ('nuvole_reservar', 'Nuvole reservar bien'),
            #  Toscana
                       ('toscana_ver', 'Toscana ver bienes'),
                       ('toscana_add', 'Toscana agregar bien'),
                       ('toscana_chag', 'Toscana cambiar bien'),
                       ('toscana_reservar', 'Toscana reservar bien'),
            #  Local Punta Oriente
                       ('local_punta_o_ver', 'Punta O local ver bienes'),
                       ('local_punta_o_add', 'Punta O local agregar bien'),
                       ('local_punta_o_chag', 'Punta O local cambiar bien'),
                       ('local_punta_o_reservar', 'Punta O local reservar bien'),
            #  Consultorio Punta Oriente
                       ('consul_punta_o_ver', 'Punta O consult ver bienes'),
                       ('consul_punta_o_add', 'Punta O consult agregar bien'),
                       ('consul_punta_o_chag', 'Punta O consult cambiar bien'),
                       ('consul_punta_o_reservar', 'Punta O consult reservar bien'),
            #  Torre Vento
                       ('torre_vento_ver', 'Torre Vento ver bienes'),
                       ('torre_vento_add', 'Torre Vento agregar bien'),
                       ('torre_vento_chag', 'Torre Vento cambiar bien'),
                       ('torre_vento_reservar', 'Torre Vento reservar bien bien'),
            #  Fracción 34
                       ('fraccion34_ver', 'Fracción 34 ver bienes'),
                       ('fraccion34_add', 'Fracción 34 agregar bien'),
                       ('fraccion34_chag', 'Fracción 34 cambiar bien'),
                       ('fraccion34_reservar', 'Fracción 34 reservar bien'),
            #  Vivienda Nuvole
                       ('vivienda_nuvole_ver', 'Nuvole viviendas ver bienes'),
                       ('vivienda_nuvole_add', 'Nuvole viviendas agregar bien'),
                       ('vivienda_nuvole_chag', ' Nuvole viviendas cambiar bien'),
                       ('vivienda_nuvole_reservar', 'Nuvole viviendas reservar bien'),
            #  Pathe
                       ('pathe_ver', 'Pathe ver bienes'),
                       ('pathe_add', 'Pathe agregar bien'),
                       ('pathe_chag', 'Pathe cambiar bien'),
                       ('pathe_reservar', 'Pathe reservar bien'),
            #  Condominio Múltiple
                       ('condom_multiple_ver', 'Condominio Múltiple ver bienes'),
                       ('condom_multiple_add', 'Condominio Múltiple agregar bien'),
                       ('condom_multiple_chag', 'Condominio Múltiple cambiar bien'),
                       ('condom_multiple_reservar', 'Condominio Múltiple reservar bien'),
        )

    def __str__(self):   # para poner los nombre en los renglones
        if self.proyecto.app == 'nuvole':
            return ' Lote: %s Manzana: %s, de la Fase: %s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.app == 'toscana':
            if self.terraza == 0:
                return ' Local: %s nivel: %s' % (self.lote, self.nivel)
            else:
                return ' Local: %s Terraza m²: %s nivel: %s' % (self.lote, self.terraza, self.nivel)
        else:
            return ""

    def _get_identificador_bien(self):
        if self.proyecto.app == 'nuvole':
            return ' Lote:%s Manzana:%s Fase:%s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.app == 'toscana':
            return ' Local:%s nivel:%s' % (self.lote, self.nivel)
        else:
            return ""
    identificador_bien = property(_get_identificador_bien)

    def _get_medidas(self):
        if self.tipo_lote == True:
            return ' Frente:%s  Fondo:%s' % (self.frente, self.fondo)
        else:
            return '%s' % (self.obs_irregular)
    medidas = property(_get_medidas)

    def _get_colindancia_norte(self):
        colindancia_norte = ""
        if not self.colindancia_norte == None:
            colindancia_norte = self.colindancia_norte
        return '%s' % (self.colindancia_norte) 
    colindancia_norte_val = property(_get_colindancia_norte)

    def _get_combo_bien(self):
        if self.proyecto.app == 'nuvole':
            return ' Lote: %s Manzana: %s, de la Fase: %s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.app == 'toscana':
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

class ComisionAgente(models.Model,PermissionRequiredMixin):
    proyecto_com = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="Proyecto_com_age")
    empleado_com = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="Empleado_com_age")
    comision = models.DecimalField('Comisión', max_digits=4, decimal_places=2, default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Comisión por asesor'
        verbose_name_plural = 'Comisiones'
        ordering = ['empleado_com','proyecto_com',]
        unique_together= (('proyecto_com','empleado_com',),)
        db_table = 'ComisionAgente'

    def __str__(self):
        return '%s %s, %s' % (self.empleado_com, self.proyecto_com, self.comsion)

class PagoComision(models.Model,PermissionRequiredMixin):
    empleado_pago = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado_pag_com")
    bien_pago = models.ForeignKey(Lote, on_delete=models.CASCADE, verbose_name="Bien_pag_com")
    modo_pago = models.IntegerField("Modo de pago", choices=MODO_PAGO, default=1)
    precio_final = models.DecimalField("Precio final", decimal_places=2, max_digits=10, default=0.00)
    enganche = models.DecimalField("Enganche", decimal_places=2, max_digits=10, null=True, blank=True, default=0.00)
    fecha_confirma_pago_adicional = models.DateField("Fecha confirmado", blank=True, null=True)
    fecha_contrato = models.DateField("Fecha de contrato", blank=True, null=True)
    comsion = models.DecimalField('Comisión', max_digits=4, decimal_places=2, default=0)
    importe = models.DecimalField("Importe comisión", decimal_places=2, max_digits=10, default=0)
    estatus_pago = models.IntegerField("Pagado",choices=RESP_SI_NO,default=False)
    fecha_pago_comision = models.DateField("Fecha pago comisión", null=True, blank=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    observacion = models.CharField("Observación", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Pago comisión'
        verbose_name_plural = 'Pago comisiones'
        ordering = ['empleado_pago','-fecha_contrato',]
        unique_together= (('bien_pago',),)
        db_table = 'PagoComision'

    def __str__(self):
        return '%s %s, %s' % (self.empleado, self.bien, self.fecha_contrato)
