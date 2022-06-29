from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView 
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from bien.models import *
from .forms import *

def index(request):
    model = Proyecto
    debug = settings.DEBUG
    template_name = 'core/index.html'
    proyectos = Proyecto.objects.filter(estatus_proyecto=1)
    ruta_imagen = ""
    if not settings.DEBUG:
        ruta_imagen = "MEDIA/"
    data = {
        'proyectos':proyectos,
        'debug':debug,
        'ruta_imagen':ruta_imagen,
    }
    return render(request, template_name, data)

class bancos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'core.view_banco'
    model = Banco
    form_class = BancoForm
    template_name = 'core/bancos.html'  
    paginate_by = settings.RENGLONES_X_PAGINA

    def get_context_data(self, **kwargs):
        context = super(bancos, self).get_context_data(**kwargs)
        return context

class nvo_banco(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'core.add_banco'
    model = Banco
    form_class = BancoForm
    template_name = 'core/nvo_banco.html'
    success_url = reverse_lazy('bancos')
    def get_context_data(self, **kwargs):
        context = super(nvo_banco, self).get_context_data(**kwargs)
        context['accion'] = "Alta"
        return context

class mod_banco(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'core.change_banco'
    model = Banco
    form_class = BancoForm
    template_name = 'core/nvo_banco.html'
    success_url = reverse_lazy('bancos')
    def get_context_data(self, **kwargs):
        context = super(mod_banco, self).get_context_data(**kwargs)
        context['accion'] = "Modifica"
        return context

def csrf_failure(request, reason=""):
    ctx = {'message': 'Hable a su administrador' }
    return render(request, 'core/mensaje.html', ctx)