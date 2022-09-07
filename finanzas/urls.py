from os import name
from django.urls import path
from .views import *

urlpatterns = [
    path('tabla_amortizacion/<pk>/<num_proyecto>/', tabla_amortizacion.as_view(), name='tabla_amortizacion'), 
    path('tabla_amort_PDF/<pk>/', tabla_amort_PDF.as_view(), name='tabla_amort_PDF'), 
    path('pagar/<num_proyecto>/', pagar.as_view(), name='pagar'), 
    path('estado_cuenta/<pk>/<num_proyecto>/', estado_cuenta.as_view(), name='estado_cuenta'), 
    path('mod_pago/<pk>/<num_proyecto>/<sol>/', mod_pago.as_view(), name='mod_pago'), 
    path('estado_cuenta_PDF/<pk>/', estado_cuenta_PDF.as_view(), name='estado_cuenta_PDF'), 
    path('lista_pagos_PDF/<pk>/<num_proyecto>/', lista_pagos_PDF.as_view(), name='lista_pagos_PDF'), 
    path('contrato_credito/<num_proyecto>/', contrato_credito.as_view(), name='contrato_credito'), 
    path('contrato_contado/<num_proyecto>/', contrato_contado.as_view(), name='contrato_contado'), 
    path('pago_comisiones/<num_proyecto>/', pago_comisiones.as_view(), name='pago_comisiones'), 
    path('pago_comisiones/<num_proyecto>/<id_periodo>/', pago_comisiones.as_view(), name='pago_comisiones'), 
    path('detalle_comisiones/<pk>/<num_proyecto>/<fecha_hasta>/<grupo>/', detalle_comisiones.as_view(), name='detalle_comisiones'), 
    path('deposito_comision/<fecha>/<num_proyecto>/<empleado>/<opcion>/', deposito_comision, name='deposito_comision'), 
    path('situacion_comisiones/<num_proyecto>/', situacion_comisiones.as_view(), name='situacion_comisiones'), 
    path('vobo_comisiones/<fecha_hasta_str>/<num_proyecto>/<fecha_hasta>/<nom_proyecto>/<imp_ger>/<imp_pub>', vobo_comisiones, name='vobo_comisiones'), 
]
 