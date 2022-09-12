from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from core.models import *
from empleado.models import Empleado

class Proyecto(models.Model):
    tipo_proyecto = models.IntegerField("Tipo de proyecto",choices=TIPO_PROYECTO,default=1)
    singular = models.CharField("Proyecto en sigular",max_length=50, default=" ")
    nombre = models.CharField("Nombre proyecto",max_length=60)
    ubicacion = models.CharField("Ubicación",max_length=250)
    estado = models.IntegerField("Estado",choices=ESTADOS, default=0)
    precio_apartir = models.DecimalField('Precio a partir', decimal_places=2, max_digits=10, default=0)
    plano = models.ImageField(upload_to="proyecto", blank=True, null=True)
    estatus_proyecto = models.IntegerField("Activo",choices=STATUS_SI_NO,default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    comision_asesor = models.DecimalField("Comision Asesor", max_digits=4, decimal_places=2, default=0)
    comision_jefe_asesor = models.DecimalField("Comision jefe Asesor", max_digits=4, decimal_places=2, default=0)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    app = models.CharField("App",max_length=20, blank=True, null=True)
    nom_proy = models.CharField("Abrev Proyecto",max_length=30, default=" ")
    fecha_alta = models.DateField("Fecha cierre proyecto", blank=True, null=True)
    fecha_cierre = models.DateField("Fecha cierre proyecto", blank=True, null=True)


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
                       ('porto_santo_acceso', 'Porto santo Acceso'),
                       ('vivienda_nuvole_acceso', 'Vivienda Nuvole Acceso'),
                       ('monte_cristallo_acceso', 'Monte cristallo Acceso'),
                       ('condom_multiple_acceso', 'Condominio Múltiple Acceso'),
                       ('comision_proyectos', 'Comisiones por proyecto'),
                       )

    def __str__(self):   # para poner los nombre en los renglones
        return '%s' % (self.nombre)

    def _get_nom_proyecto(self):
        nom_proyecto = ""
        if not self.nombre == None:
            nom_proyecto = self.nombre
        return '%s' % (nom_proyecto) 
    nom_proyecto = property(_get_nom_proyecto)
    
class Lote(models.Model, PermissionRequiredMixin):
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, verbose_name="Proyecto")  
    fase = models.SmallIntegerField("Fase", choices=FASE, default=0)
    manzana = models.SmallIntegerField("Manzana", default=0) 
    nivel = models.SmallIntegerField("Nivel", default=0) 
    lote = models.CharField("Lote",max_length=10)
    tipo_lote = models.IntegerField("Tipo de lote",choices=TIPO_LOTE, default=1)
    obs_irregular = models.CharField("Medidas",max_length=250, blank=True, null=True)
    fondo = models.DecimalField("Fondo", decimal_places=2, max_digits=10,default=0)
    frente = models.DecimalField("Frente", decimal_places=2, max_digits=10,default=0)
    total = models.DecimalField("Area", decimal_places=2, max_digits=10,default=0)
    precio_x_mt = models.DecimalField("Precio por m²", decimal_places=2, max_digits=10, default=0)
    precio = models.DecimalField("Precio", decimal_places=2, max_digits=10, default=0.00)
    terraza = models.DecimalField("Terraza m²", decimal_places=2, max_digits=10, default=0)
    precio_x_mt_t = models.DecimalField("Precio por m² terraza", decimal_places=2, max_digits=10, default=0.00)
    precio_terraza = models.DecimalField("Precio terraza", decimal_places=2, max_digits=10, default=0.00)
    precio_total = models.DecimalField("Precio total", decimal_places=2, max_digits=10, default=0.00)
    gran_total = models.DecimalField("Total gral.", decimal_places=2, max_digits=10, default=0.00)
    esquina = models.IntegerField("Esquina",choices=ESQUINA_SI, default=0)
    altura = models.DecimalField("Altura", decimal_places=2, max_digits=10, default=0)
    colindancia_norte = models.CharField("Colindancia norte",max_length=250, blank=True, null=True)
    colindancia_sur = models.CharField("Colindancia sur",max_length=250, blank=True, null=True)
    colindancia_este = models.CharField("Colindancia este",max_length=250, blank=True, null=True)
    colindancia_oeste = models.CharField("Colindancia oeste",max_length=250, blank=True, null=True)
    estatus_lote = models.IntegerField("Estatus",choices=STATUS_BIEN,default=1)
    asesor = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Asesor", null=True, blank=True)
    coordenadas = models.CharField("Coordenas", max_length=255, blank=True, null=True)
    posicion_x = models.IntegerField("Posición X numero", default=0)
    posicion_y = models.IntegerField("Posición Y numero", default=0)
    posicion_texto_x = models.IntegerField("Posición X mts", default=0)
    posicion_texto_y = models.IntegerField("Posición Y mts", default=0)
    posicion_circulo_x = models.IntegerField("Posición X circulo", default=0)
    posicion_circulo_y = models.IntegerField("Posición Y circulo", default=0)
    estacionamientos = models.IntegerField("Estacionamientos", default=0)
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
        unique_together= (('proyecto','fase','manzana','lote'),)
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
            #  Porto Santo
                       ('porto_santo_ver', 'Porto Santo ver bienes'),
                       ('porto_santo_add', 'Porto Santo agregar bien'),
                       ('porto_santo_chag', 'Porto Santo cambiar bien'),
                       ('porto_santo_reservar', 'Porto Santo reservar bien'),
            #  Vivienda Nuvole
                       ('vivienda_nuvole_ver', 'Nuvole viviendas ver bienes'),
                       ('vivienda_nuvole_add', 'Nuvole viviendas agregar bien'),
                       ('vivienda_nuvole_chag', ' Nuvole viviendas cambiar bien'),
                       ('vivienda_nuvole_reservar', 'Nuvole viviendas reservar bien'),
            #  Monte cristallo 
                       ('monte_cristallo_ver', 'Monte cristallo ver bienes'),
                       ('monte_cristallo_add', 'Monte cristallo agregar bien'),
                       ('monte_cristallo_chag', 'Monte cristallo cambiar bien'),
                       ('monte_cristallo_reservar', 'Monte cristallo reservar bien'),
            #  Condominio Múltiple
                       ('condom_multiple_ver', 'Condominio Múltiple ver bienes'),
                       ('condom_multiple_add', 'Condominio Múltiple agregar bien'),
                       ('condom_multiple_chag', 'Condominio Múltiple cambiar bien'),
                       ('condom_multiple_reservar', 'Condominio Múltiple reservar bien'),
        )

    def __str__(self):   # para poner los nombre en los renglones
        if self.proyecto.app == 'nuvole':
            return '%s Manzana: %s, de la Fase: %s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.app == 'toscana':
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            if self.terraza == 0:
                return '%s nivel: %s' % (self.lote, s_nivel)
            else:
                return '%s Terraza m²: %s nivel: %s' % (self.lote, self.terraza, s_nivel)
        elif self.proyecto.app == 'plazapuntaoriente':
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            return '%s nivel: %s' % (self.lote, s_nivel)
        else:
            return ""

    def _get_identificador_bien(self):
        if self.proyecto.app == 'nuvole':
            return '%s Manzana:%s Fase:%s' % (self.lote, self.manzana, self.fase)
        elif self.proyecto.app == 'toscana':
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            return '%s nivel:%s' % (self.lote, s_nivel)
        elif self.proyecto.app == 'plazapuntaoriente':
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            return '%s nivel:%s' % (self.lote, s_nivel)
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
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            if self.terraza == 0:
                return ' Local: %s nivel: %s' % (self.lote, s_nivel)
            else:
                return ' Local: %s Terraza: %sm² nivel: %s' % (self.lote, self.terraza, s_nivel)
        elif self.proyecto.app == 'plazapuntaoriente':
            if self.nivel == 0:
                s_nivel = "PB"
            else:
                s_nivel = self.nivel
            return ' Local: %s nivel: %s' % (self.lote, s_nivel)
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

    def _get_nom_proyecto(self):
        nom_proyecto = ""
        if not self.lote.proyecto == None:
            nom_proyecto = self.colindancia_oeste
        return '%s' % (self.colindancia_oeste) 
    colindancia_oeste_val = property(_get_colindancia_oeste)

class Estacionamiento(models.Model, PermissionRequiredMixin):
    proyecto = models.ForeignKey("Proyecto", on_delete=models.CASCADE, verbose_name="Proyecto_estac", null=True, blank=True)  
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE, verbose_name="Departamento", null=True, blank=True)
    numero = models.CharField("lugar", max_length=10, default=" ")
    frente = models.DecimalField("frente", max_digits=2, decimal_places=2, default=0)
    fondo = models.DecimalField("fondo", max_digits=2, decimal_places=2, default=0)
    total = models.DecimalField("total", max_digits=2, decimal_places=2, default=0)
    compartido = models.IntegerField("Compartido", choices=RESP_SI_NO, default=0)
    estatus_estaciona = models.IntegerField("Estatus estacionamiento", choices=STATUS_SI_NO, default=1)
    coordenadas = models.CharField("Coordenas", max_length=255, default=" ")
    posicion_x = models.IntegerField("Posición X numero", default=0)
    posicion_y = models.IntegerField("Posición Y numero", default=0)
    posicion_texto_x = models.IntegerField("Posición X mts", default=0)
    posicion_texto_y = models.IntegerField("Posición Y mts", default=0)
    posicion_circulo_x = models.IntegerField("Posición X circulo", default=0)
    posicion_circulo_y = models.IntegerField("Posición Y circulo", default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizadcurrento", auto_now=True)

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
        return '%s %s, %s' % (self.empleado_com, self.proyecto_com, self.comision)

class PagoComision(models.Model,PermissionRequiredMixin):
# detalles del bien
    proyecto_pago = models.ForeignKey(Proyecto, on_delete=models.CASCADE, verbose_name="Proyecto_pag_com")
    asesor_pago = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado_pag_com", null=True, blank=True)
    bien_pago = models.ForeignKey(Lote, on_delete=models.CASCADE, verbose_name="Bien_pag_com")
    modo_pago = models.IntegerField("Modo de pago", choices=MODO_PAGO, default=1)
    precio_final = models.DecimalField("Precio final", decimal_places=2, max_digits=10, default=0.00)
    enganche = models.DecimalField("Enganche", decimal_places=2, max_digits=10, default=0.00)
    fecha_confirma_pago_adicional = models.DateField("Fecha confirmado", blank=True, null=True)
    fecha_contrato = models.DateField("Fecha de contrato", blank=True, null=True)
# comisión asesor
    comsion = models.DecimalField('Comisión asesor', max_digits=4, decimal_places=2, default=0)
    importe = models.DecimalField("Importe comisión asesor", decimal_places=2, max_digits=10, default=0)
    folio_comision_asesor = models.IntegerField("Folio de pago comisión asesor", default=0)
    estatus_pago_asesor = models.IntegerField("Estatus comisión aasesor",choices=STATUS_GESTION_COMISION,default=0)
    fecha_deposito_comision = models.DateField("Fecha pago comisión asesor", null=True, blank=True)
    recibo_asesor_firmado = models.ImageField(upload_to="comAsesor", blank=True, null=True)
    comprobante_asesor_deposito = models.ImageField(upload_to="comAsesor", blank=True, null=True)
# comision gerente
    gerente_pago = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Gerente_pag_com",related_name="Gerente_pag_com", null=True, blank=True)
    comsion_gerente = models.DecimalField('Comisión director', max_digits=4, decimal_places=2, default=0)
    importe_gerente = models.DecimalField("Importe comisión director", decimal_places=2, max_digits=10, default=0)
    folio_comision_gerente = models.IntegerField("Folio de pago comisión director", default=0)
    estatus_pago_gerente = models.IntegerField("Estatus comisión director",choices=STATUS_GESTION_COMISION,default=0)
    fecha_deposito_comision_gerente = models.DateField("Fecha pago comisión director", null=True, blank=True)
    recibo_gerente_firmado = models.ImageField(upload_to="comGerente", blank=True, null=True)
    comprobante_gerente_deposito = models.ImageField(upload_to="comGerente", blank=True, null=True)
# comision publicidad
    comsion_publicidad = models.DecimalField('Comisión publicidad', max_digits=4, decimal_places=2, default=0)
    importe_publicidad = models.DecimalField("Importe comisión publicidad", decimal_places=2, max_digits=10, default=0)
    folio_comision_publicidad = models.IntegerField("Folio de pago comisión publicidad", default=0)
    estatus_pago_publicidad = models.IntegerField("Estatus comisión director",choices=STATUS_GESTION_COMISION,default=0)
    fecha_deposito_comision_publicidad = models.DateField("Fecha pago comisión publicidad", null=True, blank=True)
    recibo_publicidad_firmado = models.ImageField(upload_to="comPublicidad", blank=True, null=True)
    comprobante_publicidad_deposito = models.ImageField(upload_to="comPublicidad", blank=True, null=True)
# datos del registro
    fecha_periodo = models.DateField("Fecha periodo de pago", null=True, blank=True)
    estatus_comision = models.IntegerField("Estatus pago comisión periodo",choices=STATUS_COMISION,default=0)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)
    observacion = models.CharField("Observación", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Pago comisión'
        verbose_name_plural = 'Pago comisiones'
        ordering = ['asesor_pago','-fecha_contrato',]
        unique_together= (('bien_pago',),)
        db_table = 'PagoComision'

    def __str__(self):
        return '%s %s, %s' % (self.asesor_pago, self.bien_pago, self.fecha_contrato)
