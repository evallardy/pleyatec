import datetime
from datetime import date, time, timedelta
import calendar
from distutils.util import subst_vars
from xml.parsers.expat import model
from django.contrib.auth.models import  Group,User,Permission
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from bien.models import PagoComision, Proyecto,ComisionAgente
from core.models import Titulo
from empleado.models import Empleado
from gestion import models as sol
from finanzas import models as pag

def fecha_hoy():
    return datetime.date.today().strftime("%d-%m-%Y")

def fecha_hoy_amd():
    return datetime.date.today().strftime("%Y-%m-%d")

def fecha_hoy_d():
    return datetime.date.today()

def str_to_str_cambiar(fecha):
    if fecha[2:3] == '-':
        fecha_res = fecha[6:] + '-' + fecha[3:5] + '-' + fecha[0:2]
    else:
        fecha_res = fecha[8:] + '-' + fecha[5:7] + '-' + fecha[0:4]
    return fecha_res

def fecha_to_str_amd(fecha):
    dia = fecha.day
    mes = fecha.month
    anio = fecha.year
    if dia < 10:
        dia_str = '0' + str(dia)
    else:
        dia_str = str(dia)
    if mes < 10:
        mes_str = '0' + str(mes)
    else:
        mes_str = str(mes)
    return str(anio) + '-' + mes_str + '-' + dia_str

def fecha_to_str_dma(fecha):
    dia = fecha.day
    mes = fecha.month
    anio = fecha.year
    if dia < 10:
        dia_str = '0' + str(dia)
    else:
        dia_str = str(dia)
    if mes < 10:
        mes_str = '0' + str(mes)
    else:
        mes_str = str(mes)
    return dia_str + '-' + mes_str + '-' + str(anio)

def str_to_fecha_amd(fecha):
    return date(int(fecha[0:4]), int(fecha[5:7]), int(fecha[8:10])) 

def str_to_fecha_dma(fecha):
    return date(int(fecha[6:10]), int(fecha[3:5]), int(fecha[0:2])) 

def ultimo_dia_febrero(fecha):
    return calendar.monthrange(fecha.year, fecha.month)[1]

def fecha_ultimo_dia_mes(fecha):
    return date(fecha.year, fecha.month, calendar.monthrange(fecha.year, fecha.month)[1])

def fecha_inicio_dia_mes_pago(fecha):
    if fecha.day > 15:
        return date(fecha.year, fecha.month, 11)
    else:
        if fecha.month == 1:
            return date(fecha.year - 1, 12, 26)
        else:
            return date(fecha.year, fecha.month - 1, 26)

def fecha_ultimo_dia_mes_pago(fecha):
    if fecha.day > 15:
        return date(fecha.year, fecha.month, 25)
    else:
        return date(fecha.year, fecha.month, 10)

def suma_dias_fecha(fecha, dias):
    suma_dias = timedelta(dias)
    return fecha + suma_dias

def fecha_ultima_pago(num_proyecto):
    proyecto = Proyecto.objects.filter(id=num_proyecto)
    fecha_hasta = fecha_hoy_d()
    fecha_cierre = proyecto[0].fecha_cierre
    if fecha_cierre:
        if fecha_hasta > fecha_cierre:
            fecha_hasta = fecha_cierre
    if fecha_hasta.day > 15:
        fecha_hasta = fecha_ultimo_dia_mes(fecha_hasta)
    else:
        dia_hasta = 15
        fecha_hasta = date(fecha_hasta.year, fecha_hasta.month, dia_hasta)
    return fecha_hasta

def datos_fecha(num_proyecto):
    proyecto = Proyecto.objects.filter(id=num_proyecto)
    fecha_alta = proyecto[0].fecha_alta
    if fecha_alta:
        fecha_desde = fecha_alta
    else:
        fecha_desde = date(2022,1,15)

    if fecha_desde.day > 15:
        fecha_desde = fecha_ultimo_dia_mes(fecha_desde)
    else:
        dia_desde = 15
        fecha_desde = date(fecha_desde.year, fecha_desde.month, dia_desde)
    fecha_hasta = fecha_ultima_pago(num_proyecto)
    if fecha_desde.day == 15:
        inicio = 1
    else:
        inicio = 2
    datos_fecha = {}
    datos_fecha['fechas'] = []
    while fecha_hasta >= fecha_desde:
        despliegue = invierte_fecha_amd_dma(str(fecha_desde))
        datos_fecha['fechas'].insert(0,{
            'valor': str(fecha_desde),
            'despliegue': despliegue,
        })
        if inicio == 1:
            fecha_desde = fecha_ultimo_dia_mes(fecha_desde)
            inicio = 2
        else:
            if fecha_desde.month == 12:
                fecha_desde = date(fecha_desde.year + 1, 1, 15) 
            else:
                fecha_desde = date(fecha_desde.year, fecha_desde.month + 1, 15) 
            inicio = 1
    return datos_fecha

def invierte_fecha_dma_amd(fecha):
    dia = fecha[0:2]
    mes = fecha[3:5]
    anio = fecha[6:10]
    return anio + "/" + mes + "/" + dia

def invierte_fecha_amd_dma(fecha):
    dia = fecha[8:10]
    mes = fecha[5:7]
    anio = fecha[0:4]
    return dia + "/" + mes + "/" + anio

def trae_empresa(pk):
    titulo = Titulo.objects.filter(id=pk).first()
    # Nombre
    field_object = Titulo._meta.get_field('nombre')
    nombre = field_object.value_from_object(titulo)
    # RFC
    field_object = Titulo._meta.get_field('rfc')
    rfc = field_object.value_from_object(titulo)
    # Domicilio 1
    field_object = Titulo._meta.get_field('domicilio1')
    domicilio1 = field_object.value_from_object(titulo)
    # Domicilio 2
    field_object = Titulo._meta.get_field('domicilio2')
    domicilio2 = field_object.value_from_object(titulo)
    # Domicilio 3
    field_object = Titulo._meta.get_field('domicilio3')
    domicilio3 = field_object.value_from_object(titulo)
    # TelÃ©fono
    field_object = Titulo._meta.get_field('telefono')
    telefono = field_object.value_from_object(titulo)
    # correo
    field_object = Titulo._meta.get_field('correo')
    correo = field_object.value_from_object(titulo)
    empresa = {}
    empresa['titulos'] = []
    empresa['titulos'].append({
        'nombre':nombre,
        'rfc':rfc,
        'domicilio1':domicilio1,
        'domicilio2':domicilio2,
        'domicilio3':domicilio3,
        'telefono':telefono,
        'correo':correo,})
    return empresa

def administrador(id_user):
    empleado = Empleado.objects.filter(usuario=id_user)
    if empleado:
        return empleado[0].asigna_solicitud
    else:
        return 0
    return empleado[0].asigna_solicitud

def comision_asesor_proyecto(agente, proyecto):
    comisiones = ComisionAgente.objects.filter(proyecto_com=proyecto, empleado_com=agente)
    if not comisiones:
        comision = 0
    else:
        comision = comisiones[0].comision
    return comision

def comision_proyecto(proyecto):
    proyectos = Proyecto.objects.filter(id=proyecto)
    if not proyectos:
        comision = 0
    else:
        comision = proyectos[0].comision
    return comision

def comisiones_proyecto_asesores(): 
    empleados = Empleado.objects.all()
    datos = {}
    datos['comisiones'] = []
    for e in empleados:
        comision1 = comision_asesor_proyecto(e.id, 1)
        comision2 = comision_asesor_proyecto(e.id, 2)
        comision3 = comision_asesor_proyecto(e.id, 3)
        comision4 = comision_asesor_proyecto(e.id, 4)
        comision5 = comision_asesor_proyecto(e.id, 5)
        comision6 = comision_asesor_proyecto(e.id, 6)
        comision7 = comision_asesor_proyecto(e.id, 7)
        comision8 = comision_asesor_proyecto(e.id, 8)
        comision9 = comision_asesor_proyecto(e.id, 9)
        datos['comisiones'].append({
            'id': e.id,
            'nombre': e.nombre_completo,
            'comision1': comision1,
            'comision2': comision2,
            'comision3': comision3,
            'comision4': comision4,
            'comision5': comision5,
            'comision6': comision6,
            'comision7': comision7,
            'comision8': comision8,
            'comision9': comision9,
        })
    return datos

def comisiones_proyecto_asesor(asesor): 
    proyectos = Proyecto.objects.all().order_by('id')
    datos = {}
    datos['comisiones'] = []
    for p in proyectos:
        comision = comision_asesor_proyecto(asesor, p.id)
        datos['comisiones'].append({
            'id': p.id,
            'nombre': p.nombre,
            'comision': comision,
        })
    return datos
