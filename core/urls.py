from django.urls import path
from .views import bancos, cambiar_contrasena, nvo_banco, mod_banco

urlpatterns = [
    path('bancos/', bancos.as_view(), name='bancos'), 
    path('nvo_banco/', nvo_banco.as_view(), name='nvo_banco'), 
    path('mod_banco/<pk>/', mod_banco.as_view(), name='mod_banco'), 
    path('cambiar_contrasena/', cambiar_contrasena.as_view(), name='cambiar_contrasena'), 
]
