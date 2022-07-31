from django.urls import path
from .views import *

urlpatterns = [
    path('empleados', empleados.as_view(), name='empleados'), 
    path('nvo_empleado/', nvo_empleado.as_view(), name='nvo_empleado'), 
    path('mod_empleado/<pk>/', mod_empleado.as_view(), name='mod_empleado'), 
    path('comisiones_asesor', comisiones_asesor.as_view(), name='comisiones_asesor'), 
    path('comision_por_asesor/<pk>', comision_por_asesor.as_view(), name='comision_por_asesor'), 
]
 