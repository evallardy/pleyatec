import datetime
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
