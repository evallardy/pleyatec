from django.urls import path
from .views import empleados, nvo_empleado, mod_empleado

urlpatterns = [
    path('empleados', empleados.as_view(), name='empleados'), 
    path('nvo_empleado/', nvo_empleado.as_view(), name='nvo_empleado'), 
    path('mod_empleado/<pk>/', mod_empleado.as_view(), name='mod_empleado'), 
]
 