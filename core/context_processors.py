from bien.models import Proyecto
from empleado.models import Empleado

def mis_variables(request):
    proyectos = Proyecto.objects.all()
    data = {}
#   Rutina para agregar los permisos de acceso de proyecto
    for p in proyectos:
        nom_proy = p.nom_proy
        permiso_str = "bien." + nom_proy + '_' + 'acceso'
        acceso = request.user.has_perms([permiso_str])
        variable_proy = nom_proy + "_acceso"
        data[variable_proy] = acceso
    valida_proyectos =  data['nuvole_acceso'] or data['toscana_acceso'] or data['torre_vento_acceso'] or \
       data['porto_santo_acceso'] or data['vivienda_nuvole_acceso'] or \
        data['monte_cristallo_acceso'] or data['consul_punta_o_acceso'] or \
        data['local_punta_o_acceso'] or data['nuvole2_acceso']
# Si algun proyecto esta asignado
    data['valida_proyectos'] = valida_proyectos
# Si tiene permisos para comisiones
    permiso_str = "bien." + 'comision_proyectos'
    acceso = request.user.has_perms([permiso_str])
    data['comision_proyectos'] = acceso
# Datos del empleado
    empleado = Empleado.objects.filter(usuario=request.user.id)
    if empleado:
        data['administrador'] = empleado[0].asigna_solicitud
        data['id_empleado'] = empleado[0].id
    else:
        data['administrador'] = False
        data['id_empleado'] = 0
    return data