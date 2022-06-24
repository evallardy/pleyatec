from django.urls import path
from .views import bancos, nvo_banco, mod_banco

urlpatterns = [
    path('bancos/', bancos.as_view(), name='bancos'), 
    path('nvo_banco/', nvo_banco.as_view(), name='nvo_banco'), 
    path('mod_banco/<pk>/', mod_banco.as_view(), name='mod_banco'), 
]
