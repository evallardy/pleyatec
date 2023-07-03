from multiprocessing import context
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from .models import *
from django.views.generic import ListView, CreateView, UpdateView 
from django.urls import reverse_lazy, reverse
from .forms import BienForm, FormaBienValida, ProyectoForm, FormaBien
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.db.models import Count

class nuvole(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.nuvole_acceso'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('py',0)
        proyecto = Proyecto.objects.filter(id=num_proyecto)
        nom_proy = proyecto[0].nom_proy
#  Acceso Nuvole
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'app_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion mapa Nuvole
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
# Contador de estados de los lotes
        bienes = Lote.objects.filter(proyecto_id=num_proyecto).values('estatus_lote').annotate(total=Count('id'))
        context["bienes"] = bienes
        context["proyecto"] = Proyecto.objects.filter(id=num_proyecto)
        context['menu'] = "menuMapa"
        return context
    def get_queryset(self):
        num_proyecto = self.kwargs.get('py',0)
        queryset = Lote.objects.filter(proyecto_id=num_proyecto)
        return queryset

class toscana(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.toscana_acceso'
    template_name = 'bien/toscana.html'  
    def get_queryset(self):
        nivel = self.kwargs['nivel']
        num_proyecto = self.kwargs['py']
#        num_proyecto = self.kwargs.get('py',0)
        queryset = Lote.objects.filter(proyecto_id=num_proyecto, nivel=nivel)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(toscana, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs['py']
#        num_proyecto = self.kwargs.get('py',0)
        proyecto = Proyecto.objects.filter(id=num_proyecto)
        nom_proy = proyecto[0].nom_proy
# Contador de estados de los lotes
        bienes = Lote.objects.filter(proyecto_id=num_proyecto).values('estatus_lote').annotate(total=Count('id'))
        context["bienes"] = bienes        
#  Acceso Toscana
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'app_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  nom_proy = 'toscana'
        context["proyecto"] = proyecto
        context['menu'] = "menuMapa"
        nivel = self.kwargs['nivel']
        context['nivel'] = nivel
        if nivel == '0':
            context['nivel_0'] = "active"
            context['nivel_1'] = ""
            context['nivel_2'] = ""
        elif nivel == '1':
            context['nivel_0'] = ""
            context['nivel_1'] = "active"
            context['nivel_2'] = ""
        else:
            context['nivel_2'] = ""
            context['nivel_1'] = ""
            context['nivel_2'] = "active"
#  Menu opcion mapa Toscana
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context

class plazapuntaoriente(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.local_punta_o_acceso'
    template_name = 'bien/plazapuntaoriente.html'  
    def get_context_data(self, **kwargs):
        context = super(plazapuntaoriente, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs['py']
        proyecto = Proyecto.objects.filter(id=num_proyecto)
        nom_proy = proyecto[0].nom_proy
        context["proyecto"] = Proyecto.objects.filter(id=num_proyecto)
        context['menu'] = "menuMapa"
#  Acceso local punta oriente
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'app_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion mapa local punta opriente
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        num_proyecto = self.kwargs['py']
        queryset = Lote.objects.filter(proyecto_id=num_proyecto)
        return queryset

class torrevento(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.torre_vento_acceso'
    template_name = 'bien/torrevento.html'  
    def get_context_data(self, **kwargs):
        context = super(torrevento, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs['py']
        context["proyecto"] = Proyecto.objects.filter(id=num_proyecto)
        context['menu'] = "menuMapa"
        nom_proy = 'torre_vento'
#  Acceso torre vento
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'app_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
# Contador de estados de los lotes
        bienes = Lote.objects.filter(proyecto_id=num_proyecto).values('estatus_lote').annotate(total=Count('id'))
        context["bienes"] = bienes
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class condominioM(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.condom_multiple_acceso'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "menuMapa"
        nom_proy = 'condom_multiple'
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class porto_santo(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.porto_santo_acceso'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "menuMapa"
        nom_proy = 'porto_santo'
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class viviendaNuvole(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.vivienda_nuvole_acceso'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "menuMapa"
        nom_proy = 'vivienda_nuvole'
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class monte_cris(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.monte_cristallo_acceso'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "menuMapa"
        nom_proy = 'monte_cristallo'
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class TMpuntaorienta(LoginRequiredMixin, ListView):
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "menuMapa"
        nom_proy = 'consul_punta_o'
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        variable_html = 'menu_proy' + des_permiso
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_proy] = acceso
        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class bienes(LoginRequiredMixin, ListView):
    template_name = 'bien/lotes.html'
    queryset = Lote.objects.all().filter(proyecto=1)
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(bienes, self).get_context_data(**kwargs)
        proyecto = self.kwargs.get('proyecto',0)
        context['menu'] = "bien"
        proyecto_tb = Proyecto.objects.all().filter(id=proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# ver listado bienes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Agregar bien        
        des_permiso = '_add'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cambiar bien        
        des_permiso = '_chag'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion lotes
        des_permiso = '_ver'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion contratar
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion pagos
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion archivo
        des_permiso = '_consulta_archivo'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion creditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Menu opcion contados
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def get_queryset(self):
        proyecto = self.kwargs.get('proyecto',0)
        queryset = Lote.objects.filter(proyecto_id=proyecto)
        return queryset

class nvo_bien(LoginRequiredMixin, CreateView):
    model = Lote
#    form_class = BienForm
    form_class = FormaBien
    template_name = 'bien/nvo_bien.html'
    def get_context_data(self, **kwargs):
        context1 = super(nvo_bien, self).get_context_data(**kwargs)
        context = carga_bienes(self, context1)
        context['accion'] = 'Alta'

        return context
    def get_success_url(self):
        num_proyecto = self.kwargs.get('proyecto',0)
        return reverse('bienes', kwargs={'proyecto': num_proyecto})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        proyecto = self.kwargs.get('proyecto')
        fase = request.POST.get('fase')
        manzana = request.POST.get('manzana')
        lote = request.POST.get('lote')
        tipo_lote = request.POST.get('tipo_lote')
        obs_irregular = request.POST.get('obs_irregular')
        fondo = request.POST.get('fondo')
        frente = request.POST.get('frente')
        esquina = request.POST.get('esquina')
        colindancia_norte = request.POST.get('colindancia_norte')
        colindancia_sur = request.POST.get('colindancia_sur')
        colindancia_este = request.POST.get('colindancia_este')
        colindancia_oeste = request.POST.get('colindancia_oeste')
        altura = request.POST.get('altura')
        estacionamientos = request.POST.get('estacionamientos')
        estatus_lote = request.POST.get('estatus_lote')
        total = float(request.POST["total"].replace(',',''))
        precio_x_mt = float(request.POST["precio_x_mt"].replace(',',''))
        precio = float(request.POST["precio"].replace(',',''))
        terraza = float(request.POST["terraza"].replace(',',''))
        precio_x_mt_t = float(request.POST["precio_x_mt_t"].replace(',',''))
        precio_terraza = float(request.POST["precio_terraza"].replace(',',''))
        gran_total = float(request.POST["gran_total"].replace(',',''))
        precio_total = float(request.POST["precio_total"].replace(',',''))
        data = {
            'proyecto':proyecto,
            'fase':fase,
            'manzana':manzana,
            'lote':lote,
            'tipo_lote':tipo_lote,
            'obs_irregular':obs_irregular,
            'fondo':fondo,
            'frente':frente,
            'total':total,
            'precio_x_mt':precio_x_mt,
            'precio':precio,
            'esquina':esquina,
            'colindancia_norte':colindancia_norte,
            'colindancia_sur':colindancia_sur,
            'colindancia_este':colindancia_este,
            'colindancia_oeste':colindancia_oeste,
            'terraza':terraza,
            'precio_x_mt_t':precio_x_mt_t,
            'precio_terraza':precio_terraza,
            'altura':altura,
            'estacionamientos':estacionamientos,
            'gran_total':gran_total,
            'precio_total':precio_total,
            'estatus_lote':estatus_lote,
        }
        lote_valida = FormaBien(data)
        if lote_valida.is_valid():
            lote_valida.save()
            return HttpResponseRedirect(reverse('bienes', kwargs={'proyecto':proyecto},))
        else:
            context1 = {}
            context = carga_bienes(self, context1)
            num_proyecto = self.kwargs.get('proyecto',0)
            context['num_proyecto'] = num_proyecto
            context['form'] = form
            return render(self.request, self.template_name, context)

def carga_bienes(self, context):
        num_proyecto = self.kwargs.get('proyecto',0)
        context['menu'] = "bien"
        context['num_proyecto'] = num_proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        #  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
        # Reservar bien        
        des_permiso = '_reservar'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        # Agregar bien        
        des_permiso = '_add'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        # Cambiar bien        
        des_permiso = '_chag'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        tipo_lote = self.request.POST.get('tipo_lote')
        if not tipo_lote:
                tipo_lote = 1
                frente = 0
                fondo = 0
                total = 0
                precio_x_mt = 0
                terraza = 0
                precio_x_mt_t = 0
        else:
                frente = self.request.POST.get('frente')
                fondo = self.request.POST.get('fondo')
                total = self.request.POST.get('total')
                precio_x_mt = self.request.POST.get('precio_x_mt')
                terraza = self.request.POST.get('terraza')
                precio_x_mt_t = self.request.POST.get('precio_x_mt_t')
        context["tipo_lote"] = tipo_lote
        context['frente'] = frente
        context['fondo'] = fondo
        context['total'] = total
        context['precio_x_mt'] = precio_x_mt
        context['terraza'] = terraza
        context['precio_x_mt_t'] = precio_x_mt_t
        return context

class mod_bien(LoginRequiredMixin, UpdateView):
    model = Lote
    form_class = FormaBien
    template_name = 'bien/nvo_bien.html'
    def get_context_data(self, **kwargs):
        context = super(mod_bien, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('proyecto',0)
        pk = self.kwargs.get('pk',0)
        context['accion'] = 'Modifica'
        context['menu'] = "bien"
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
        inf_lote = Lote.objects.filter(id=pk)
        context['inf_lote'] = inf_lote
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Reservar bien        
        des_permiso = '_reservar'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Agregar bien        
        des_permiso = '_add'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cambiar bien        
        des_permiso = '_chag'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def get_success_url(self):
        num_proyecto = self.kwargs.get('proyecto',0)
        return reverse('bienes', kwargs={'proyecto': num_proyecto})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        proyecto = self.kwargs.get('proyecto')
        pk = self.kwargs.get('pk',0)
        fase = request.POST.get('fase')
        manzana = request.POST.get('manzana')
        lote = request.POST.get('lote')
        tipo_lote = request.POST.get('tipo_lote')
        obs_irregular = request.POST.get('obs_irregular')
        fondo = request.POST.get('fondo')
        frente = request.POST.get('frente')
        esquina = request.POST.get('esquina')
        colindancia_norte = request.POST.get('colindancia_norte')
        colindancia_sur = request.POST.get('colindancia_sur')
        colindancia_este = request.POST.get('colindancia_este')
        colindancia_oeste = request.POST.get('colindancia_oeste')
        altura = request.POST.get('altura')
        estacionamientos = request.POST.get('estacionamientos')
        estatus_lote = request.POST.get('estatus_lote')
        total = float(request.POST["total"].replace(',',''))
        precio_x_mt = float(request.POST["precio_x_mt"].replace(',',''))
        precio = float(request.POST["precio"].replace(',',''))
        terraza = float(request.POST["terraza"].replace(',',''))
        precio_x_mt_t = float(request.POST["precio_x_mt_t"].replace(',',''))
        precio_terraza = float(request.POST["precio_terraza"].replace(',',''))
        gran_total = float(request.POST["gran_total"].replace(',',''))
        precio_total = float(request.POST["precio_total"].replace(',',''))
        data = {
            'proyecto':proyecto,
            'fase':fase,
            'manzana':manzana,
            'tipo_lote':tipo_lote,
            'obs_irregular':obs_irregular,
            'fondo':fondo,
            'frente':frente,
            'total':total,
            'precio_x_mt':precio_x_mt,
            'precio':precio,
            'esquina':esquina,
            'colindancia_norte':colindancia_norte,
            'colindancia_sur':colindancia_sur,
            'colindancia_este':colindancia_este,
            'colindancia_oeste':colindancia_oeste,
            'terraza':terraza,
            'precio_x_mt_t':precio_x_mt_t,
            'precio_terraza':precio_terraza,
            'altura':altura,
            'estacionamientos':estacionamientos,
            'gran_total':gran_total,
            'precio_total':precio_total,
            'estatus_lote':estatus_lote,
        }
        lote_valida = FormaBienValida(data)
        lote_upd = Lote.objects.get(id=pk)
        lote_upd.fase = fase
        lote_upd.manzana = manzana
        lote_upd.tipo_lote = tipo_lote
        lote_upd.obs_irregular = obs_irregular
        lote_upd.fondo = fondo
        lote_upd.frente = frente
        lote_upd.total = total
        lote_upd.precio_x_mt = precio_x_mt
        lote_upd.precio = precio
        lote_upd.esquina = esquina
        lote_upd.colindancia_norte = colindancia_norte
        lote_upd.colindancia_sur = colindancia_sur
        lote_upd.colindancia_este = colindancia_este
        lote_upd.colindancia_oeste = colindancia_oeste
        lote_upd.terraza = terraza
        lote_upd.precio_x_mt_t = precio_x_mt_t
        lote_upd.precio_terraza = precio_terraza
        lote_upd.altura = altura
        lote_upd.estacionamientos = estacionamientos
        lote_upd.gran_total = gran_total
        lote_upd.precio_total = precio_total
        lote_upd.estatus_lote = estatus_lote
        if lote_valida.is_valid():
            lote_act = Lote.objects.filter(id=pk)
            if lote_act[0].lote != lote:
                lote_act = Lote.objects.filter(proyecto=proyecto,fase=fase,manzana=manzana,lote=lote)
                if not lote_act:
                    lote_upd.lote = lote
            lote_upd.save()
            return HttpResponseRedirect(reverse('bienes', kwargs={'proyecto':proyecto},))
        else:
            context1 = {}
            context = carga_bienes(self, context1)
            num_proyecto = self.kwargs.get('proyecto',0)
            context['pk'] = pk
            context['form'] = form
            context['accion'] = 'Modifica'
            context['menu'] = "bien"
            proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
            context['proyecto_tb'] = proyecto_tb
            context['num_proyecto'] = num_proyecto
            inf_lote = Lote.objects.filter(id=pk)
            context['inf_lote'] = inf_lote
            return render(self.request, self.template_name, context)

class proyectos(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'bien/proyectos.html'  
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(proyectos, self).get_context_data(**kwargs)
        permiso_str = "bien." + 'comision_proyectos'
        acceso = self.request.user.has_perms([permiso_str])
        context['comision_proyectos'] = acceso
        proyecto_tb = Proyecto.objects.all()
        for py in proyecto_tb:
            nom_proy = py.nom_proy
            nom_acceso = nom_proy + '_edita_comisiones_proyecto'
            permiso_str = "finanzas." + nom_acceso
            acceso = self.request.user.has_perms([permiso_str])
            context[nom_acceso] = acceso
            nom_acceso = nom_proy + '_pago_normal_comisiones'
            permiso_str = "finanzas." + nom_acceso
            acceso = self.request.user.has_perms([permiso_str])
            context[nom_acceso] = acceso
            nom_acceso = nom_proy + '_consulta_comisiones'
            permiso_str = "finanzas." + nom_acceso
            acceso = self.request.user.has_perms([permiso_str])
            context[nom_acceso] = acceso
        return context
    def get_queryset(self):
        queryset = Proyecto.objects.all()
        return queryset

class mod_proyecto(LoginRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'bien/nvo_proyecto.html'
    success_url = reverse_lazy('proyectos')
    def get_context_data(self, **kwargs):
        context = super(mod_proyecto, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        proyecto = Proyecto.objects.filter(id=pk)
        nom_proy = proyecto[0].nom_proy
        permiso_str = 'finanzas.' + nom_proy + '_edita_comisiones_proyecto'
        acceso = self.request.user.has_perms([permiso_str])
        context['app_proy_edita_comisiones_proyecto'] = acceso
        nombre = proyecto[0].nombre
        context['nombre'] = nombre
        context['accion'] = "Modifica"
        context['proyecto'] = proyecto
        return context
