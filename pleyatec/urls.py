from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls.conf import include

from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='index'),
    path('bien/', include('bien.urls')),
    path('gestion/', include('gestion.urls')),
    path('empleado/', include('empleado.urls')),
    path('cliente/', include('cliente.urls')),
    path('core/', include('core.urls')),
    path('finanzas/', include('finanzas.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }), 
]

#urlpatterns +=  [
#    re_path(r'^media/(?P<path>.*)$', serve, {
#        'document_root': settings.MEDIA_ROOT,
#    })
#]

#urlpatterns += [
#    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
#]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += [
#    re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT,})
#]
