from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView 
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from bien.models import *
from .forms import *

def index(request):
    model = Proyecto
    template_name = 'core/index.html'
    proyectos = Proyecto.objects.filter(estatus_proyecto=1)
    ruta_imagen = ""
    data = {
        'proyectos':proyectos,
        'ruta_imagen':ruta_imagen,
    }
#   Rutina para agregar los permisos de acceso de proyecto
    for p in proyectos:
        nom_proy = p.nom_proy
        permiso_str = "bien." + nom_proy + '_' + 'acceso'
        acceso = request.user.has_perms([permiso_str])
        variable_proy = nom_proy + "_acceso"
        data[variable_proy] = acceso
    data['prueba'] = 123456
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