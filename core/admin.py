from django.contrib import admin
from .models import *
from bien.models import *
from cliente.models import *
from gestion.models import *
from finanzas.models import *
from empleado.models import *


admin.site.register(Banco)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proyecto)
admin.site.register(Lote)
admin.site.register(Solicitud)
admin.site.register(Folios)
admin.site.register(Pago)
admin.site.register(Titulo)
admin.site.register(PagoComision)
admin.site.register(ComisionAgente)
