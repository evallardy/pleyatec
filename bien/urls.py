from django.urls import path
from .views import *

urlpatterns = [
    # Proyecto 1 
    path('nuvole/<py>/', nuvole.as_view(), name='nuvole'), 
    # Proyecto 1 
    path('toscana/<py>/<nivel>/', toscana.as_view(), name='toscana'), 
    # Proyecto 3 
    path('torrevento/<py>/<nivel>/', torrevento.as_view(), name='torrevento'), 
    # Proyecto 4 
    path('monte_cris/<py>/', monte_cris.as_view(), name='monte_cris'), 
    # Proyecto 5 
    path('viviendaNuvole/<py>/', viviendaNuvole.as_view(), name='viviendaNuvole'), 
    # Proyecto 6 
    path('porto_santo/<py>/<nivel>/', porto_santo.as_view(), name='porto_santo'), 
    # Proyecto 7 
    path('TMpuntaorienta/<py>/<nivel>/', TMpuntaorienta.as_view(), name='TMpuntaorienta'), 
    # Proyecto 8
    path('plazapuntaoriente/<py>/<nivel>/', plazapuntaoriente.as_view(), name='plazapuntaoriente'), 
    # Proyecto 9 
    path('condominioM/<py>/<nivel>/', condominioM.as_view(), name='condominioM'), 
    

    path('bienes/<proyecto>/', bienes.as_view(), name='bienes'), 
    path('nvo_bien/<proyecto>/', nvo_bien.as_view(), name='nvo_bien'), 
    path('mod_bien/<pk>/<proyecto>/', mod_bien.as_view(), name='mod_bien'), 

    path('proyectos/', proyectos.as_view(), name='proyectos'), 
    path('mod_proyecto/<pk>/', mod_proyecto.as_view(), name='mod_proyecto'), 
]
