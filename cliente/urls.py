from django.urls import path
from .views import clientes, nvo_cliente, mod_cliente

urlpatterns = [
    path('clientes/', clientes.as_view(), name='clientes'), 
    path('nvo_cliente/', nvo_cliente.as_view(), name='nvo_cliente'), 
    path('mod_cliente/<pk>/', mod_cliente.as_view(), name='mod_cliente'), 
]
