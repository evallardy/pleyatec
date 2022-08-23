from errno import ESTALE
from core.models import COMISION_PUBLICIDAD
from empleado.models import Empleado
from bien.models import ComisionAgente, Lote, PagoComision, Proyecto
from .models import Folios, Regla
from django.db.models import Max

def f_asigna_solicitud(self):
    usuario = self.request.user.id
    empleado = Empleado.objects.filter(usuario=usuario).first()
    if empleado == None:
        asigna_solicitud = False
    else:
        field_object = Empleado._meta.get_field('asigna_solicitud')
        asigna_solicitud = field_object.value_from_object(empleado)
    return asigna_solicitud

def f_empleado(self):
    usuario = self.request.user.id
    empleado = Empleado.objects.filter(usuario=usuario).first()
    if empleado == None:
        id_empleado = 0
    else:
        field_object = Empleado._meta.get_field('id')
        id_empleado = field_object.value_from_object(empleado)
    return id_empleado

def comision_asesor(asesor, proyecto, director):
    reg_comision = ComisionAgente.objects.filter(proyecto_com=proyecto,empleado_com=asesor)
    comision = 0
    if reg_comision:
        comision = reg_comision[0].comision
    if comision == 0:
        reg_comision_proyecto = Proyecto.objects.filter(id=proyecto)
        if reg_comision_proyecto:
            if director:
                comision = reg_comision_proyecto[0].comision_jefe_asesor
            else:
                comision = reg_comision_proyecto[0].comision_asesor
    return comision

def genera_comision(asesor, lote, modo_pago, precio_final, enganche, fecha_confirma_pago_adicional, fecha_contrato):
    lote = Lote.objects.filter(id=lote)
    id_proyecto = lote[0].proyecto.id
    comision = comision_asesor(asesor, id_proyecto, False)
    jefe = Empleado.objects.filter(id=asesor)
    director = jefe[0].subidPersdonal
    comision_director = comision_asesor(director, id_proyecto, True)
    comision_publicidad = COMISION_PUBLICIDAD
    importe = precio_final * comision / 100
    importe_director = precio_final * comision_director / 100
    importe_publicidad = precio_final * comision_publicidad / 100
    pagoComision = PagoComision(empleado_pago_id=asesor, bien_pago_id=lote, modo_pago=modo_pago, \
        precio_final=precio_final, enganche=enganche, fecha_confirma_pago_adicional=fecha_confirma_pago_adicional, \
        fecha_contrato=fecha_contrato, comsion=comision, importe=importe, comsion_director=comision_director, \
        importe_director=importe_director, comsion_publicidad=comision_publicidad, importe_publicidad=importe_publicidad)
    return pagoComision

def nuevo_folio(tipo):
    folio = Folios.objects.filter(tipo=tipo).aggregate(Max('numero'))['numero__max']
    if folio == None:
        folio = 1
    else:
        folio += 1
    return folio

def regla_descuento(id_proyecto, precio_lote, metros2, mensualidades):
    if precio_lote == '':
        precio_lote = 0
    if metros2 == '':
        metros2 = 0
    if mensualidades == '':
        mensualidades = 0
    regla = Regla.objects.filter(proyecto=id_proyecto)
    tipo_aplica_descto = regla[0].tipo_aplica_descto
    valor1 = regla[0].valor1
    if tipo_aplica_descto == 1:
        return valor1 * metros2
    elif tipo_aplica_descto == 2:
        return valor1
    elif tipo_aplica_descto == 3:
        return precio_lote * valor1 / 100
    elif tipo_aplica_descto == 4:
        for mens in regla:
            valor1 = regla[0].valor1
            if mens.mensualidades_permitidas == mensualidades:
                return valor1
        return 0
    elif tipo_aplica_descto == 5:
        for mens in regla:
            valor1 = regla[0].valor1
            if mens.mensualidades_permitidas == mensualidades:
                return precio_lote * valor1 / 100
        return 0
    else:
        return 0

def regla_apartado_min(id_proyecto, importe):
    regla = Regla.objects.filter(proyecto=id_proyecto)
    tipo_apartado_minimo = regla[0].tipo_apartado_minimo
    valor2 = regla[0].valor2
    if tipo_apartado_minimo == 1:
        return valor2
    elif tipo_apartado_minimo == 2:
        return importe * valor2 / 100
    else:
        return 0

def regla_enganche_min(id_proyecto, importe):
    regla = Regla.objects.filter(proyecto=id_proyecto)
    tipo_enganche_minimo = regla[0].tipo_enganche_minimo
    valor3 = regla[0].valor3
    if tipo_enganche_minimo == 1:
        return valor3
    elif tipo_enganche_minimo == 2:
        return importe * valor3 / 100
    else:
        return 0

def regla_mesualidades_permitidas(id_proyecto):
    return Regla.objects.filter(proyecto=id_proyecto)
