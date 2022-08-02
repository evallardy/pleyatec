import datetime
from distutils.util import subst_vars
from xml.parsers.expat import model
from bien.models import Proyecto,ComisionAgente
from core.models import Titulo
from empleado.models import Empleado
from django.contrib.auth.models import  Group,User,Permission
from django.contrib.auth.models import User

def fecha_hoy():
    return datetime.datetime.now().strftime("%d-%m-%Y")

def datos_fecha(num_proyecto):
    proyecto = Proyecto.objects.filter(id=num_proyecto)
    fecha_alta = proyecto[0].fecha_alta
    fecha_cierre = proyecto[0].fecha_cierre
    fecha_hoy = fecha_hoy()
    fecha_hasta = str(fecha_hoy)
    if fecha_cierre:
        if fecha_hoy1 > fecha_cierre:
            fecha_hasta = str(fecha_cierre)

    if fecha_alta:
        fecha_desde = str(fecha_alta)
    else:
        fecha_desde = '2022/01/15'


        if fecha_hoy1 > fecha_cierre:
            fecha_hasta = str(fecha_cierre)


    fecha_hoy1 = datetime.datetime.strptime(fecha_hoy(), '%d-%m-%Y')
    if fecha_hoy1.day > 15:
        if fecha_hoy1.mes == 2:
            if fecha_hoy1.year % 4 == 0:
                dia = "29"
            else:
                dia = "28"
        else:
            dia = "30"
    else:
        dia = "15"
    mes = fecha_hoy1.month
    anio = str(fecha_hoy1.year)
    if mes < 10:
        mes_str = "0" + str(mes)
    else:
        mes_str = str(mes)
    fecha_hasta = anio + "/" + mes_str + "/" + dia

#    fecha_desde = "2022/01/15"
    anio_desde = proyecto[0].fecha_alta.year
    mes_desde = proyecto[0].fecha_alta.month
    if proyecto[0].fecha_alta.day <= 15:
        inicio = 1
    else:
        inicio = 2
    if proyecto[0].fecha_cierre.day <= 15:
        inicio = 1
    else:
        inicio = 2

    datos_fecha = {}
    datos_fecha['fechas'] = []
    while fecha_hasta >= fecha_desde:
        valor = fecha_desde
        despliegue = invierte_fecha_amd_dma(fecha_desde)
        datos_fecha['fechas'].insert(0,{
            'valor': valor,
            'despliegue': despliegue,
        })
        if mes_desde < 10:
            mes_desde1 = "0" + str(mes_desde)
        else:
            mes_desde1 = str(mes_desde)
        if inicio == 1:
            if mes_desde == 2:
                if anio_desde % 4 == 0:
                    fecha_desde = str(anio_desde) + "/" + mes_desde1 + "/" + "29"
                else:
                    fecha_desde = str(anio_desde) + "/" + mes_desde1 + "/" + "28"
            else:
                fecha_desde = str(anio_desde) + "/" + mes_desde1 + "/" + "30"
            inicio = 2
        else:
            mes_desde += 1
            if mes_desde > 12:
                mes_desde = 1
                anio_desde += 1
            if mes_desde < 10:
                mes_desde1 = "0" + str(mes_desde)
            else:
                mes_desde1 = mes_desde
            fecha_desde = str(anio_desde) + "/" + mes_desde1 + "/" + "15"
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