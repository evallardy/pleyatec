import os
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Max, Q, Subquery
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import View
from django.template.loader import get_template
from time import gmtime, strftime
from xhtml2pdf import pisa
import numpy as np

from finanzas.models import Pago

from .models import *
from .funciones import *
from .forms import *
from core.numero_letras import numero_a_letras
from core.funciones import fecha_hoy, trae_empresa

class solicitudes(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gestion.view_solicitud'
    model = Solicitud
    context_object_name = 'obj'
    template_name = 'gestion/solicitudes.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        num_proyecto = self.kwargs.get('num_proyecto')
        asigna_solicitud = f_asigna_solicitud(self)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(solicitudes, self).get_context_data(**kwargs)
        context['menu'] = "solicitud"
        num_proyecto = self.kwargs.get('num_proyecto')
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context

class nva_solicitud(CreateView):
    permission_required = 'gestion.add_solicitud'
    model = Solicitud
    form_class = Nuvole_SolicitudForm
    context_object_name = 'obj'
    template_name = 'gestion/nva_solicitud.html'
    def get_context_data(self, **kwargs):
        context = super(nva_solicitud, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['lote_cmb'] = Lote.objects.filter(proyecto=num_proyecto,estatus_lote=1).all()
        if 'empleado_cmb' not in context:
            asigna_solicitud = f_asigna_solicitud(self)
            f_emp = f_empleado(self)
            if asigna_solicitud:
                query1 = Q(tipo_empleado='E', area_operativa=5)
                query2 = Q(id=f_emp)
                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                    .order_by('paterno','materno','nombre').all()
                context['f_emp'] = 0
            else:
                empleado_cmb = Empleado.objects.filter(id=f_emp) \
                    .order_by('paterno','materno','nombre')
                context['f_emp'] = f_emp
            context['empleado_cmb'] = empleado_cmb
#        context['form'] = self.form_class(self.request.GET)
        context['menu'] = "solicitud"
        context['accion'] = "Alta"
        context['sol'] = Solicitud.objects.filter(id = 0)
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            solicitud1 = form.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
    
class mod_solicitud(UpdateView): 
    permission_required = 'gestion.change_solicitud'
    model = Solicitud
    form_class = Nuvole_SolicitudForm
    template_name = 'gestion/nva_solicitud.html'
    def get_context_data(self, **kwargs):
        context = super(mod_solicitud, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        solicitud = self.model.objects.get(id=pk)
        context['lote_cmb'] = Lote.objects.filter(proyecto=num_proyecto,estatus_lote=1).all()
        if 'empleado_cmb' not in context:
            asigna_solicitud = f_asigna_solicitud(self)
            if asigna_solicitud:
                query1 = Q(tipo_empleado='E', area_operativa=5)
                query2 = Q(id=f_empleado(self))
                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                    .order_by('paterno','materno','nombre').all()
            else:
                empleado_cmb = Empleado.objects.filter(id=f_empleado(self)) \
                    .order_by('paterno','materno','nombre')
            context['empleado_cmb'] = empleado_cmb
#        context['form'] = self.form_class()
        context['menu'] = "solicitud"
        context['accion'] = "Modifica"
        context['id'] = pk
        context['sol'] = Solicitud.objects.filter(id = pk)
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = kwargs['pk']
        solicitud = self.model.objects.get(id=id_solicitud)
        form = self.form_class(request.POST, request.FILES, instance=solicitud)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})

def can_sol(request, llave, num_proyecto):
    sol = Solicitud.objects.filter(id=llave).update(estatus_solicitud='99', apartado=0)
    return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto},))

def rec_sol(request, llave, num_proyecto):
    sol = Solicitud.objects.filter(id=llave).update(estatus_solicitud='1')
    return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto} ,))

class autorizaciones(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('gestion.autoriza_visualiza')
    model = Solicitud
    second_model = Lote
    context_object_name = 'obj'
    template_name = 'gestion/autorizaciones.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(estatus_solicitud__in=[5,99]) \
                .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
            .filter(asesor_id=id_empleado) \
            .exclude(estatus_solicitud__in=[5,99]) \
            .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        return queryset
    def get_context_data(self, **kwargs):
        context = super(autorizaciones, self).get_context_data(**kwargs)
        context['menu'] = "autorizacion"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context

def aut_ventas(request, llave, num_proyecto):
     sol = Solicitud.objects.filter(id=llave).update(aprobacion_gerente=True)
     return HttpResponseRedirect(reverse(('autorizaciones'), kwargs={'num_proyecto':num_proyecto} ,))

def aut_desarrollo(request, llave, num_proyecto):
    sol = Solicitud.objects.filter(id=llave).update(aprobacion_director=True)
    return HttpResponseRedirect(reverse(('autorizaciones'), kwargs={'num_proyecto':num_proyecto} ,))

class compromisos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gestion.compromiso'
    model = Solicitud
    second_model = Lote
    context_object_name = 'obj'
    template_name = 'gestion/compromisos.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        return queryset
    def get_context_data(self, **kwargs):
        context = super(compromisos, self).get_context_data(**kwargs)
        context['menu'] = "compromiso"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        return context

class pagos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): 
    permission_required = 'gestion.pago_compromiso'
    model = Solicitud
    form_class = Nuvole_SolicitudForm
    template_name = 'gestion/pagos.html'
    def get_context_data(self, **kwargs):
        context = super(pagos, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto
        context['pk'] = pk
        pk = self.kwargs.get('pk',0)
        context['sol'] = Solicitud.objects.filter(id=pk)
        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk',0)
        queryset = Solicitud.objects.all().filter(id=pk)
        return queryset
    def post(self, request, *args, **kwargs):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        paga = request.POST.get( 'paga')
        pk = self.kwargs.get('pk',0)
        apartado = float(request.POST.get('apartado'))
        pago_adicional = float(request.POST.get('pago_adicional'))
        lote_id = request.POST.get('lote')
        solicitud = Solicitud.objects.filter(id=pk).update(estatus_solicitud=paga, apartado=apartado, pago_adicional=pago_adicional)
        lote = Lote.objects.filter(id=lote_id).update(estatus_lote=paga)
        return HttpResponseRedirect(reverse(('compromisos'), kwargs={'num_proyecto':num_proyecto} ,))

class archivo(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gestion.consulta_archivo'
#    model = Solicitud
    second_model = Lote
    template_name = 'gestion/archivo_solicitudes.html'
#    lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=1)
#    queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk')))
    paginate_by = settings.RENGLONES_X_PAGINA

    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk')))
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(archivo, self).get_context_data(**kwargs)
        context['menu'] = "archivo"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        return context

class reciboPDF(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'gestion.pago_compromiso'
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
#        try:
        template = get_template('gestion/reciboPDF.html')
        hoy = fecha_hoy()
        pk=self.kwargs['pk']
        solicitud = Solicitud.objects.all().filter(id=pk).first()
        pago = self.kwargs['desc']
        if pago == "parcial":
            field_object = Solicitud._meta.get_field('num_apartado')
            num_recibo = field_object.value_from_object(solicitud)
            field_object = Solicitud._meta.get_field('apartado')
            importe = field_object.value_from_object(solicitud)
        else: # pago total
            field_object = Solicitud._meta.get_field('num_adicional')
            num_recibo = field_object.value_from_object(solicitud)
            field_object = Solicitud._meta.get_field('pago_adicional')
            importe = field_object.value_from_object(solicitud)
        if num_recibo == 0:
            num_recibo = Folios.objects.filter(tipo=1).aggregate(Max('numero'))['numero__max']
            if num_recibo == None:
                num_recibo = 1
            else:
                num_recibo += 1
            dato = solicitud.lote.lote + " manzana: " + \
                str(solicitud.lote.manzana) + " fase: " + str(solicitud.lote.fase) + \
                " del proyecto: " + str(solicitud.lote.proyecto)
            observacion = "Solicitud " + str(solicitud.id) + ": Comprobante de pago " + pago + " del lote: " + dato
            folio = Folios(
                tipo = 1, 
                numero = num_recibo,
                observacion = observacion,
                importe = importe)
            folio.save()
            if pago == "parcial":
                sol = Solicitud.objects.filter(id=self.kwargs['pk'])   \
                    .update(num_apartado=num_recibo)
            else:
                sol = Solicitud.objects.filter(id=self.kwargs['pk'])   \
                    .update(num_adicional=num_recibo)
        importe_letras = numero_a_letras(importe)
        copias = [0,1]
        empresa=trae_empresa(1)
        context = {
            'comp': {
                'numero_recibo': num_recibo, 
                'empresa':empresa['titulos'][0]['nombre'],
                'rfc':empresa['titulos'][0]['rfc'],
                'ubicacion1':empresa['titulos'][0]['domicilio1'],
                'ubicacion2':empresa['titulos'][0]['domicilio2'],
                'ubicacion3':empresa['titulos'][0]['telefono'],
                'hoy':hoy,
                'importe': importe,
                'importe_letras': importe_letras,
                'pago':pago,
            },
            'copias':copias,
            'solicitud':solicitud,
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, 
            dest=response,
            link_callback=self.link_callback,
        )
        return response
 #       except:
 #           pass
 #       return HttpResponseRedirect(reverse_lazy('recibosPDF'))

class contratos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gestion.contratar'
    model = Solicitud
    second_model = Lote
    context_object_name = 'obj'
    template_name = 'gestion/contratos.html'
    paginate_by = settings.RENGLONES_X_PAGINA

    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=1)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) 
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10])  
        return queryset

    def get_context_data(self, **kwargs):
        context = super(contratos, self).get_context_data(**kwargs)
        context['menu'] = "contrata"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        if num_proyecto == '1':
            context['reporte'] = "/gestion/contratoPDF/"
            context['reporte1'] = "/finanzas/lista_pagos_PDF/"
        elif num_proyecto == '2':
            context['reporte'] = "/gestion/contratoPDF/"
            context['reporte1'] = "/finanzas/lista_pagos_PDF/"
        return context

class datos_contrato(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): 
    permission_required = 'gestion.datos_contrato'
    model = Solicitud
    form_class = DatosContratoForm
    context_object_name = 'obj'
    template_name = 'gestion/datos_contrato.html'
    def get_context_data(self, **kwargs):
        context = super(datos_contrato, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        solicitud = self.model.objects.get(id=pk)
        context["obj"] = Solicitud.objects.filter(pk=pk).first()
        context['form'] = self.form_class()
        context['id'] = pk
        context['solicitud'] = solicitud
        context['menu'] = "contrata"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        context['proyecto'] = Proyecto.objects.filter(id=num_proyecto)
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = kwargs['pk']
        solicitud = self.model.objects.get(id=id_solicitud)
        #  Estatus solicitud
        field_object = Solicitud._meta.get_field('estatus_solicitud')
        estatus_solicitud = field_object.value_from_object(solicitud)
        #  Cantidad de pagos
        field_object = Solicitud._meta.get_field('cantidad_pagos')
        cantidad_pagos = field_object.value_from_object(solicitud)
        #  Pago mensual
        field_object = Solicitud._meta.get_field('importe_x_pago')
        importe_x_pago = field_object.value_from_object(solicitud)
        #  Enganche
        field_object = Solicitud._meta.get_field('enganche')
        enganche = field_object.value_from_object(solicitud)
        #  Modo pago
        field_object = Solicitud._meta.get_field('modo_pago')
        modo_pago = field_object.value_from_object(solicitud)
        #  Pago final
        field_object = Solicitud._meta.get_field('precio_final')
        precio_final = field_object.value_from_object(solicitud)
        diferencia = precio_final - enganche

        form = self.form_class(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            if modo_pago == 1:
                sol = Solicitud.objects.filter(id=self.kwargs['pk']) \
                    .update(estatus_solicitud=9)
            else:
                sol = Solicitud.objects.filter(id=self.kwargs['pk']) \
                    .update(estatus_solicitud=10)
                pk = self.kwargs.get('pk',0)
                anio = int(request.POST.get('anio_inicio_pago'))
                mes = request.POST.get('mes_inicio_pago')
                anio_hasta = anio + 3
                num_pago = 1
                anios = np.arange(anio,anio_hasta,1,int) 
                meses = np.arange(1,13,1,int) 
                diferencia -= importe_x_pago
                encontro = False
                for  a in anios:
                    for m in meses:
                        if m == int(mes) or encontro:
                            encontro = True
                            if m < 10:
                                fecha_pago = str(a) + "-0" + str(m) + "-01"     
                            else:
                                fecha_pago = str(a) + "-" + str(m) + "-01" 
                            pago = Pago(convenio=solicitud, numero_pago=num_pago, importe=importe_x_pago, \
                                fecha_pago=fecha_pago)
                            pago.save()
                            if num_pago == cantidad_pagos:
                                return HttpResponseRedirect(self.get_success_url())                
                            num_pago +=1
                            if diferencia < importe_x_pago:
                                importe_x_pago = diferencia
                            else:
                                diferencia -= importe_x_pago
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url()) 
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        return reverse_lazy('contratos', kwargs={'num_proyecto': num_proyecto})


def archiva(request, id, estado, num_proyecto):
    if estado == "6":
        archiva_solicitud = Solicitud.objects.filter(id=id).update(estatus_solicitud = 7)
    else:
        if estado == "99":
            archiva_solicitud = Solicitud.objects.filter(id=id).update(estatus_solicitud = 8)
    return reverse_lazy('contratos', kwargs={'num_proyecto': num_proyecto})
#    return HttpResponseRedirect(reverse_lazy('contratos'))

class contratoPDF(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'gestion.imprime_contrato'
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path
    def get(self, request, *args, **kwargs):
        hoy = fecha_hoy()
        solicitud = Solicitud.objects.all().filter(id=self.kwargs['pk']).first()
        template = get_template('gestion/contratoPDF.html')
        field_object1 = Solicitud._meta.get_field('num_contrato')
        num_contrato = field_object1.value_from_object(solicitud)

        field_object2 = Solicitud._meta.get_field('apartado')
        apartado = field_object2.value_from_object(solicitud)

        field_object3 = Solicitud._meta.get_field('pago_adicional')
        pago_adicional = field_object3.value_from_object(solicitud)

        lote = Lote.objects.all().filter(id=solicitud.lote_id).first()

        field_object4 = lote._meta.get_field('total')
        total = field_object4.value_from_object(lote)

        field_object5 = Solicitud._meta.get_field('precio_final')
        precio_final = field_object5.value_from_object(solicitud)
        precio_final_i = int(precio_final)
        precio_final_d = str(abs(precio_final) - abs(int(precio_final)))[-2:]
        precio_final_l = numero_a_letras(precio_final_i)

        field_object6 = Solicitud._meta.get_field('cantidad_pagos')
        cantidad_pagos = field_object6.value_from_object(solicitud)
        cantidad_pagos_l = numero_a_letras(cantidad_pagos)
        cantidad_pagos_1 = cantidad_pagos - 1


        field_object7 = lote._meta.get_field('precio')
        precio = field_object7.value_from_object(lote)
        precio_i = int(precio)
        precio_d = str(abs(precio) - abs(int(precio)))[-2:]
        precio_l = numero_a_letras(precio_i)

        field_object8 = lote._meta.get_field('precio_x_mt')
        precio_x_mt = field_object8.value_from_object(lote)
        precio_x_mt_i = int(precio_x_mt)
        precio_x_mt_d = str(abs(precio_x_mt) - abs(int(precio_x_mt)))[-2:]
        precio_x_mt_l = numero_a_letras(precio_x_mt_i)

        field_object8 = solicitud._meta.get_field('enganche')
        enganche = field_object8.value_from_object(solicitud)
        enganche_i = int(enganche)
        enganche_d = str(abs(enganche) - abs(int(enganche)))[-2:]
        enganche_l = numero_a_letras(enganche_i)

        field_object8 = solicitud._meta.get_field('importe_x_pago')
        importe_x_pago = field_object8.value_from_object(solicitud)
        importe_x_pago_i = int(importe_x_pago)
        importe_x_pago_d = str(abs(importe_x_pago) - abs(int(importe_x_pago)))[-2:]

        saldo = precio_final - enganche
        saldo_i = int(saldo)
        saldo_d = str(abs(saldo) - abs(int(saldo)))[-2:]
        saldo_l = numero_a_letras(saldo_i)

        importe_total_x_pagos = importe_x_pago * cantidad_pagos

        ultimo_pago = importe_x_pago - (importe_total_x_pagos - saldo)
        ultimo_pago_i = int(ultimo_pago)
        ultimo_pago_d = str(abs(ultimo_pago) - abs(int(ultimo_pago)))[-2:]

        field_object9 = solicitud._meta.get_field('porcentaje_descuento')
        porcentaje_descuento = (100 - field_object9.value_from_object(solicitud)) / 100
        precio_x_mt_n = round(precio_x_mt * porcentaje_descuento,2)
        precio_x_mt_n_i = int(precio_x_mt_n)
        precio_x_mt_n_d = str(abs(precio_x_mt_n) - abs(int(precio_x_mt_n)))[-2:]
        precio_x_mt_n_l = numero_a_letras(precio_x_mt_n_i)

        field_object10 = solicitud._meta.get_field('modo_pago')
        modo_pago = field_object10.value_from_object(solicitud)

        field_object11 = solicitud._meta.get_field('fecha_contrato')
        fecha_contrato = field_object11.value_from_object(solicitud)

        fecha_contrato_anio_s = str(fecha_contrato.year)

        if num_contrato != 0:
            num_contrato = num_contrato
        else: 
            num_contrato = Folios.objects.filter(tipo=2).aggregate(Max('numero'))['numero__max']
            if num_contrato == None:
                num_contrato = 1
            else:
                num_contrato += 1
            if modo_pago == 1 or modo_pago == 3:
                esta_sol = 6
            else:
                esta_sol = 10
            dato = str(solicitud.lote) + \
                " del proyecto: " + str(solicitud.lote.proyecto)
            observacion = "Contrato del " + dato
            folio = Folios(
                tipo = 2, 
                numero = num_contrato,
                observacion = observacion,
                importe = precio_final)
            folio.save()
            sol = Solicitud.objects.filter(id=self.kwargs['pk'])   \
                .update(num_contrato=num_contrato, estatus_solicitud=esta_sol)
        importe_letras = numero_a_letras(apartado)
        importe_letras_t = numero_a_letras(pago_adicional)
        metro_letras = numero_a_letras(total)
        copias = [0,1]
        context = {
            'comp': {
                'num_contrato': num_contrato,
                'empresa':'Pleyatec, S.A. de C.V.',
                'rfc':'AAA-333333333',
                'ubicacion1':'Av. Constituyentes #1009, Interior No. 5, Col. Residencial del valle, C.P 76190,',
                'ubicacion2':'Santiago de QuerÃ©taro, Qro.',
                'ubicacion3':'Tel: 442-138-5840',
                'hoy':hoy,
                'importe_letras': importe_letras,
                'importe_letras_t': importe_letras_t,
                'metros_letra':metro_letras,
            },
            'ahora':hoy,
            'copias':copias,
            'solicitud':solicitud,
            'lote':lote,
            'precio_final':precio_final,
            'precio_final_i':precio_final_i,
            'precio_final_d':precio_final_d,
            'precio_final_l':precio_final_l,
            'cantidad_pagos':cantidad_pagos,
            'cantidad_pagos_l':cantidad_pagos_l,
            'cantidad_pagos_1':cantidad_pagos_1,
            'precio_x_mt':precio_x_mt,
            'precio_x_mt_i':precio_x_mt_i,
            'precio_x_mt_d':precio_x_mt_d,
            'precio_x_mt_l':precio_x_mt_l,
            'precio':precio,
            'precio_i':precio_i,
            'precio_d':precio_d,
            'precio_l':precio_l,
            'enganche':enganche,
            'enganche_i':enganche_i,
            'enganche_d':enganche_d,
            'enganche_l':enganche_l,
            'importe_x_pago':importe_x_pago,
            'importe_x_pago_i':importe_x_pago_i,
            'importe_x_pago_d':importe_x_pago_d,
            'saldo':saldo,
            'saldo_i':saldo_i,
            'saldo_d':saldo_d,
            'saldo_l':saldo_l,
            'precio_x_mt_n':precio_x_mt_n,
            'precio_x_mt_n_i':precio_x_mt_n_i,
            'precio_x_mt_n_d':precio_x_mt_n_d,
            'precio_x_mt_n_l':precio_x_mt_n_l,
            'ultimo_pago':ultimo_pago,
            'ultimo_pago_i':ultimo_pago_i,
            'ultimo_pago_d':ultimo_pago_d,
            'fecha_contrato_anio_s':fecha_contrato_anio_s,
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, 
            dest=response,
            link_callback=self.link_callback,
        )
        if 'menu' not in context:
            context['menu'] = "contrata"
        return response
 #       except:
 #           pass
 #       return HttpResponseRedirect(reverse_lazy('recibosPDF'))
