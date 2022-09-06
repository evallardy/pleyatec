from errno import ESTALE
from core.models import AREA_OPERATIVA, COMISION_PUBLICIDAD, PUESTO
from empleado.models import Empleado
from bien.models import ComisionAgente, Lote, PagoComision, Proyecto
from .models import Folios, Regla
from django.db.models import Max

def f_asigna_solicitud(self):
    usuario = self.request.user.id
    empleado = Empleado.objects.filter(usuario=usuario)
    if not empleado:
        asigna_solicitud = 0
    else:
        asigna_solicitud = empleado[0].asigna_solicitud
    return asigna_solicitud

def  f_empleado(self):
    usuario = self.request.user.id
    empleado = Empleado.objects.filter(usuario=usuario)
    if not empleado:
        id_empleado = 0
    else:
        id_empleado = empleado[0].id
    return id_empleado

def  f_area_puesto(self):
    num_area = AREA_OPERATIVA
    num_puesto = PUESTO
    usuario = self.request.user.id
    empleado = Empleado.objects.filter(usuario=usuario)
    if not empleado:
        area_operativa = 0
        puesto = 0
    else:
        area_operativa = empleado[0].area_operativa
        puesto = empleado[0].puesto
    datos = {
        'puesto':puesto,
        'area_operativa':area_operativa,
    }
    return datos

def obtener_comision(asesor, proyecto, gerente):
    reg_comision = ComisionAgente.objects.filter(proyecto_com=proyecto,empleado_com=asesor)
    comision = 0
    if reg_comision:
        comision = reg_comision[0].comision
    if comision == 0:
        reg_comision_proyecto = Proyecto.objects.filter(id=proyecto)
        if reg_comision_proyecto:
            if gerente:
                comision = reg_comision_proyecto[0].comision_jefe_asesor
            else:
                comision = reg_comision_proyecto[0].comision_asesor
    return comision

def genera_comision(asesor, lote, modo_pago, precio_final, enganche, fecha_confirma_pago_adicional, fecha_contrato):
    lote = Lote.objects.filter(id=lote)
    id_proyecto = lote[0].proyecto.id
    comision = obtener_comision(asesor, id_proyecto, False)
    jefe = Empleado.objects.filter(id=asesor)
    gerente = jefe[0].subidPersonal
    comision_gerente = obtener_comision(gerente, id_proyecto, True)
    comision_publicidad = COMISION_PUBLICIDAD
    importe = precio_final * comision / 100
    importe_gerente = precio_final * comision_gerente / 100
    importe_publicidad = precio_final * comision_publicidad / 100
    pagoComision = PagoComision(asesor_pago_id=asesor, bien_pago_id=lote, modo_pago=modo_pago, \
        precio_final=precio_final, enganche=enganche, fecha_confirma_pago_adicional=fecha_confirma_pago_adicional, \
        fecha_contrato=fecha_contrato, comsion=comision, importe=importe, comsion_gerente=comision_gerente, \
        importe_gerente=importe_gerente, comsion_publicidad=comision_publicidad, \
        importe_publicidad=importe_publicidad,gerente_pago=gerente)
    return pagoComision

def nuevo_folio(tipo):
    folio = Folios.objects.filter(tipo=tipo).aggregate(Max('numero'))['numero__max']
    if not folio:
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
