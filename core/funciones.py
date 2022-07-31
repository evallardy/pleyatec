import datetime
from xml.parsers.expat import model
from bien.models import Proyecto,ComisionAgente
from core.models import Titulo
from empleado.models import Empleado
from django.contrib.auth.models import  Group,User,Permission
from django.contrib.auth.models import User

def fecha_hoy():
    return datetime.datetime.now().strftime("%d-%m-%Y")

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