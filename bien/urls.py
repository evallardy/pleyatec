from django.urls import path
from .views import *

urlpatterns = [
    path('nuvole/', nuvole.as_view(), name='nuvole'), 
    path('toscana/<nivel>/', toscana.as_view(), name='toscana'), 

    path('torrevento/<nivel>/', torrevento.as_view(), name='torrevento'), 
    path('condominioM/<nivel>/', condominioM.as_view(), name='condominioM'), 
    path('porto_santo/<nivel>/', porto_santo.as_view(), name='porto_santo'), 
    path('viviendaNuvole/', viviendaNuvole.as_view(), name='viviendaNuvole'), 
    path('monte_cris/', monte_cris.as_view(), name='monte_cris'), 
    path('TMpuntaorienta/<nivel>/', TMpuntaorienta.as_view(), name='TMpuntaorienta'), 
    path('plazapuntaoriente/<nivel>/', plazapuntaoriente.as_view(), name='plazapuntaoriente'), 

    path('bienes/<proyecto>/', bienes.as_view(), name='bienes'), 
    path('nvo_bien/<proyecto>/', nvo_bien.as_view(), name='nvo_bien'), 
    path('mod_bien/<pk>/<proyecto>/', mod_bien.as_view(), name='mod_bien'), 

    path('proectos/', proyectos.as_view(), name='proyectos'), 
    path('mod_proyecto/<pk>/', mod_proyecto.as_view(), name='mod_proyecto'), 
]
