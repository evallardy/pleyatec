from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Empleado
from .forms import EmpleadoForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.conf import settings

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
