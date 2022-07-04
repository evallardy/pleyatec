from django.urls import path
from .views import *

urlpatterns = [
    path('nuvole/', nuvole.as_view(), name='nuvole'), 
    path('toscana/<nivel>/', toscana.as_view(), name='toscana'), 

    path('torrevento/<nivel>/', torrevento.as_view(), name='torrevento'), 
    path('condominioM/<nivel>/', condominioM.as_view(), name='condominioM'), 
    path('fraccion34/<nivel>/', fraccion34.as_view(), name='fraccion34'), 
    path('viviendaNuvole/', viviendaNuvole.as_view(), name='viviendaNuvole'), 
    path('pathe/', pathe.as_view(), name='pathe'), 
    path('TMpuntaorienta/<nivel>/', TMpuntaorienta.as_view(), name='TMpuntaorienta'), 
    path('plazapuntaoriente/<nivel>/', plazapuntaoriente.as_view(), name='plazapuntaoriente'), 

    path('bienes/<proyecto>/', bienes.as_view(), name='bienes'), 
    path('nvo_bien/<proyecto>/', nvo_bien.as_view(), name='nvo_bien'), 
    path('mod_bien/<pk>/<proyecto>/', mod_bien.as_view(), name='mod_bien'), 

]
