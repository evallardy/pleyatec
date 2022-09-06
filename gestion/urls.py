from os import name
from django.urls import path
from .views import *

urlpatterns = [
    path('solicitudes/<num_proyecto>/', solicitudes.as_view(), name='solicitudes'), 
    path('nva_solicitud/<num_proyecto>/', nva_solicitud.as_view(), name='nva_solicitud'), 
    path('mod_sol/<pk>/<num_proyecto>/', mod_solicitud.as_view(), name='mod_solicitud'),
    path('can_sol/<llave>/<num_proyecto>/', can_sol, name='can_sol'),
    path('rec_sol/<llave>/<num_proyecto>/', rec_sol, name='rec_sol'),
    path('autorizaciones/<num_proyecto>/', autorizaciones.as_view(), name='autorizaciones'),
    path('aut_ventas/<llave>/<num_proyecto>/', aut_ventas, name='aut_ventas'),
    path('aut_desarrollo/<llave>/<num_proyecto>/', aut_desarrollo, name='aut_desarrollo'),
    path('compromisos/<num_proyecto>/', compromisos.as_view(), name='compromisos'),
    path('pagos/<pk>/<num_proyecto>/', pagos.as_view(), name='pagos'),
    path('archivo/<num_proyecto>/', archivo.as_view(), name='archivo'),
    path('reciboPDF/<pk>/<desc>/', reciboPDF.as_view(), name='reciboPDF'),
    path('contratos/<num_proyecto>/', contratos.as_view(), name='contratos'), 
    path('contratoPDF/<pk>/<num_proyecto>/', contratoPDF.as_view(), name='contratoPDF'),
    path('datos_contrato/<pk>/<num_proyecto>/', datos_contrato.as_view(), name='datos_contrato'),
    path('archiva/<id>/<estado>/<num_proyecto>/', archiva, name='archiva'),
]