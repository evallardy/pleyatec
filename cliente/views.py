from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings

from .models import Cliente
from empleado.models import Empleado
from .forms import ClienteForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from core.funciones import administrador


class clientes(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'cliente.view_cliente'
    model = Cliente
    template_name = 'cliente/clientes.html'  
    paginate_by = settings.RENGLONES_X_PAGINA

    def get_context_data(self, **kwargs):
        context = super(clientes, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        if administrador(self.request.user.id):
            queryset = Cliente.objects.filter(estatus_cliente=1)
        else:
            empleado = Empleado.objects.filter(usuario=self.request.user.id)
            id_empleado = empleado[0].id
            queryset = Cliente.objects.filter(estatus_cliente=1,asesor=id_empleado)
        return queryset

class nvo_cliente(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'cliente.add_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/nvo_cliente.html'
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super(nvo_cliente, self).get_context_data(**kwargs)
        context['accion'] = "Alta"
#        context["administrador"] = administrador(self.request.user.id)
        return context

class mod_cliente(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'cliente.change_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente/nvo_cliente.html'
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        context = super(mod_cliente, self).get_context_data(**kwargs)
        context['accion'] = "Modifica"
 #       context["administrador"] = administrador(self.request.user.id)
        return context
