from django.urls import path
from .views import *

urlpatterns = [
    path('nuvole/', nuvole.as_view(), name='nuvole'), 
    path('toscana/<nivel>/', toscana.as_view(), name='toscana'), 
    path('bienes/<proyecto>/', bienes.as_view(), name='bienes'), 
    path('nvo_bien/<proyecto>/', nvo_bien.as_view(), name='nvo_bien'), 
    path('mod_bien/<pk>/<proyecto>/', mod_bien.as_view(), name='mod_bien'), 

]
