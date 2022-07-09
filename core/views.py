from re import template
from django.conf import settings
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView 
from django.shortcuts import redirect, render
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
#    for p in proyectos:
#        nom_proy = p.nom_proy
#        permiso_str = "bien." + nom_proy + '_' + 'acceso'
#        acceso = request.user.has_perms([permiso_str])
#        variable_proy = nom_proy + "_acceso"
#        data[variable_proy] = acceso
#    valida_proyectos =  data['nuvole_acceso'] or data['toscana_acceso'] or data['torre_vento_acceso'] or \
#        data['condom_multiple_acceso'] or data['fraccion34_acceso'] or data['vivienda_nuvole_acceso'] or \
#        data['pathe_acceso'] or data['consul_punta_o_acceso'] or data['local_punta_o_acceso']
#    data['valida_proyectos'] = valida_proyectos
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

class cambiar_contrasena(LoginRequiredMixin, View):
    template_name = 'core/cambiar_contrasena.html'
    form_class = CambiaContrasenaForm
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs ):
        return render(request, self.template_name, {'form': self.form_class})
    
    def post(self, request, *args, **kwargs ):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(id=request.user.id)
            if user.exists(): 
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})

