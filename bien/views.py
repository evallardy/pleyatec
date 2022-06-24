from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, CreateView, UpdateView 
from django.urls import reverse_lazy, reverse
from .forms import BienForm
from django.conf import settings
from django.http.response import HttpResponseRedirect

class nuvole(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.view_lote'
    template_name = 'bien/nuvole.html'  
    def get_context_data(self, **kwargs):
        context = super(nuvole, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=1)
        context['menu'] = "lote"

        return context
    def get_queryset(self):
        queryset = Lote.objects.filter(proyecto_id=1)
        return queryset

class toscana(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.view_lote'
    template_name = 'bien/toscana.html'  
    def get_queryset(self):
        nivel = self.kwargs['nivel']
        queryset = Lote.objects.filter(proyecto_id=2, nivel=nivel)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(toscana, self).get_context_data(**kwargs)
        context["proyecto"] = Proyecto.objects.filter(id=2)
        context['menu'] = "lote"
        nivel = self.kwargs['nivel']
        context['nivel'] = nivel
        if nivel == '1':
            context['nivel_1'] = "active"
            context['nivel_2'] = ""
            context['nivel_3'] = ""
        elif nivel == '2':
            context['nivel_1'] = ""
            context['nivel_2'] = "active"
            context['nivel_3'] = ""
        else:
            context['nivel_1'] = ""
            context['nivel_2'] = ""
            context['nivel_3'] = "active"
        return context

class bienes(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'bien.view_lote'
    template_name = 'bien/lotes.html'
    queryset = Lote.objects.all().filter(proyecto=1)
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(bienes, self).get_context_data(**kwargs)
        proyecto = self.kwargs.get('proyecto',0)
        context['menu'] = "bien"
        context['proyecto'] = Proyecto.objects.filter(id=proyecto)
        return context
    def get_queryset(self):
        proyecto = self.kwargs.get('proyecto',0)
        queryset = Lote.objects.filter(proyecto_id=proyecto)
        return queryset

class nvo_bien(CreateView):
    permission_required = 'bien.add_lote'
    model = Lote
    form_class = BienForm
    template_name = 'bien/nvo_bien.html'
    def get_context_data(self, **kwargs):
        context = super(nvo_bien, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('proyecto',0)
        context['accion'] = 'Alta'
        context['menu'] = "lote"
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context
    def get_success_url(self):
        num_proyecto = self.kwargs.get('proyecto',0)
        return reverse('bienes', kwargs={'proyecto': num_proyecto})

class mod_bien(UpdateView):
    permission_required = 'bien.change_lote'
    model = Lote
    form_class = BienForm
    template_name = 'bien/nvo_bien.html'
    def get_context_data(self, **kwargs):
        context = super(mod_bien, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('proyecto',0)
        context['accion'] = 'Modifica'
        context['menu'] = "lote"
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context
    def get_success_url(self):
        num_proyecto = self.kwargs.get('proyecto',0)
        return reverse('bienes', kwargs={'proyecto': num_proyecto})
