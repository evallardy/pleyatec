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
    path('lista_pagos_PDF/<pk>/', lista_pagos_PDF.as_view(), name='lista_pagos_PDF'), 
]
 