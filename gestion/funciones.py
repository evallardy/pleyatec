from empleado.models import Empleado

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
