from ast import Not
from multiprocessing import context
import re
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.http.response import HttpResponseRedirect
from core.funciones import comisiones_proyecto_asesores, comisiones_proyecto_asesor, comision_asesor_proyecto
from .models import Empleado
from bien.models import Proyecto
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from bien.models import ComisionAgente

class empleados(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'empleado.view_empleado'
    model = Empleado
    template_name = 'empleado/empleados.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(empleados, self).get_context_data(**kwargs)
        return context

class nvo_empleado(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'empleado.add_empleado'
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/nvo_empleado.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('empleados')
    def get_context_data(self, **kwargs):
        context = super(nvo_empleado, self).get_context_data(**kwargs)
        context['accion'] = "Alta"
        return context

class mod_empleado(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'empleado.change_empleado'
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado/nvo_empleado.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('empleados')
    def get_context_data(self, **kwargs):
        context = super(mod_empleado, self).get_context_data(**kwargs)
        context['accion'] = "Modifica"
        return context

class comisiones_asesor(LoginRequiredMixin, ListView):
    template_name = 'empleado/comisiones_asesor.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(comisiones_asesor, self).get_context_data(**kwargs)
        empleados = Empleado.objects.all()
        context['empleados'] = empleados
        context['datos'] = comisiones_proyecto_asesores()
        return context
    def get_queryset(self):
        queryset = Proyecto.objects.all().order_by('id')
        return queryset

class comision_por_asesor(LoginRequiredMixin, ListView):
    form_class = EmpleadoComisionForm
    template_name = 'empleado/nvo_comision.html'
    success_url = reverse_lazy('comisiones_asesor')
    def get_context_data(self, **kwargs):
        context = super(comision_por_asesor, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        comisiones_asesor = Empleado.objects.filter(id=pk)
        context['nombre_empleado'] = comisiones_asesor[0].nombre_completo
        mensaje = self.kwargs.get('mensaje')
        if not mensaje:
            mensaje = ''
        context['mensaje'] = mensaje
        proyectos_cmb = Proyecto.objects.all()
        context['proyectos_cmb'] = proyectos_cmb
        context['accion'] = "Comisiones"
        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk',0)
        queryset = ComisionAgente.objects.filter(empleado_com=pk).order_by('proyecto_com')
        return queryset
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        proyecto = request.POST.get('proyecto')
        comision = request.POST.get('comision')
        proyecto_comision = ComisionAgente.objects.filter(proyecto_com=proyecto,empleado_com=pk)
        if comision == '.':
            mensaje = 'Comisión inválida'
        else:
            comision_num = float(comision)
            if proyecto_comision:
                if comision_num == 0:
                    # Eliminar registgro
                    comision_accion = ComisionAgente.objects.filter(proyecto_com=proyecto,empleado_com=pk) \
                        .delete()
                    mensaje = 'Se eleminó la comisión'
                else:
                    # Actualizar registro
                    if comision_num > 0 and comision_num < 30:
                        comision_accion = ComisionAgente.objects.filter(proyecto_com=proyecto,empleado_com=pk) \
                            .update(comision=comision_num)
                        mensaje = 'Se actualizó la comisión'
                    else:
                        mensaje = 'Comisión no modificada'
            else:
                # Alta del registro
                if comision_num > 0 and comision_num < 30:
                    comision_accion = ComisionAgente(
                            proyecto_com_id = proyecto, 
                            empleado_com_id = pk,
                            comision = comision_num)
                    comision_accion.save()
                    mensaje = 'Se agregó la comisión'
                else:
                    mensaje = 'Comisión no agregada'
        return HttpResponseRedirect(reverse('comision_por_asesor', kwargs={'pk':pk,'mensaje':mensaje}))
