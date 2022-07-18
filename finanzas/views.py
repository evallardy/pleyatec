from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import os
import datetime
from django.conf import settings
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, View
from django.template.loader import get_template
from django.http.response import HttpResponse, HttpResponseRedirect
from time import gmtime, strftime
from xhtml2pdf import pisa
from django.db.models import Subquery
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models.aggregates import Count
from django.db.models import Sum

from django.shortcuts import render

from bien.models import Proyecto, Lote
from core.models import Titulo
from .funciones import datos_tabla_amortizacion
from core.funciones import fecha_hoy, trae_empresa
from gestion.models import Solicitud
from gestion.funciones import f_asigna_solicitud, f_empleado
from finanzas.models import Pago
from .forms import PagoForm

class tabla_amortizacion(TemplateView):
    template_name = 'finanzas/tabla_amortizacion.html'
    def get_context_data(self, **kwargs):
        context = super(tabla_amortizacion, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        datos = datos_tabla_amortizacion(pk)
        solicitud = Solicitud.objects.filter(id=pk).first()
        context['solicitud'] = solicitud
        context['id'] = pk
        context['datos'] = datos
        context['menu'] = "solicitud"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context["proyecto_tb"] = proyecto_tb
        context['num_proyecto'] = num_proyecto
        context['archivo'] = '/finanzas/tabla_amort_PDF/'
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado amortizacion solicitud
        des_permiso = '_amortizac'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Impresión Listado amortizacion solicitud
        des_permiso = '_imprime_amortizac'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context

class tabla_amort_PDF(View):
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
        context = {}
        template = get_template('finanzas/tabla_amort_PDF.html')
        pk = self.kwargs['pk']
        datos = datos_tabla_amortizacion(pk)
        solicitud = Solicitud.objects.filter(id=pk).first()
        hoy = fecha_hoy()
        empresa = trae_empresa(1)
        context['solicitud'] = solicitud
        context['datos'] = datos
        context['menu'] = "solicitud"
        context['hoy'] = hoy
        context['empresa'] = empresa
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, 
            dest=response,
            link_callback=self.link_callback,
        )
        return response

class pagar(ListView):
    model = Solicitud
    template_name = 'finanzas/pagar.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud=10) 
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .filter(estatus_solicitud=10) 
        return queryset

    def get_context_data(self, **kwargs):
        context = super(pagar, self).get_context_data(**kwargs)
        context['menu'] = "pagar"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado de mensualidades
        des_permiso = '_listado_registro_mensual'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Estado de cuenta
        des_permiso = '_estado_cuenta'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
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
'''
class pagos(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): 
    permission_required = 'gestion.pago_compromiso'
    model = Solicitud
    second_model = Lote
    tercer_model = Cliente
    quart_model = Empleado
    form_class = Nuvole_SolicitudForm
    second_form_class = Num_LoteForm
    context_object_name = 'obj'
    template_name = 'gestion/pagos.html'
    success_url = reverse_lazy('pagos' )
    def get_context_data(self, **kwargs):
        context = super(pagos, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        solicitud = self.model.objects.get(id=pk)
        lote = self.second_model.objects.get(id=solicitud.lote_id)
        cliente = self.tercer_model.objects.get(id=solicitud.cliente_id)
        asesor = self.quart_model.objects.get(id=solicitud.asesor_id)
        context["obj"] = Solicitud.objects.filter(pk=pk).first()
        context['lote'] = lote
        context['cliente'] = cliente
        context['asesor'] = asesor
        context['form'] = self.form_class()
        context['form2'] = self.second_form_class(instance=lote)
        context['menu'] = "compromiso"
        context['id'] = pk
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_solicitud = kwargs['pk']
        solicitud = self.model.objects.get(id=id_solicitud)
        id_lote = solicitud.lote_id
        estatus_solicitud = solicitud.estatus_solicitud
        lote = self.second_model.objects.get(id=solicitud.lote_id)
        form = self.form_class(request.POST, instance=solicitud)
        form2 = self.second_form_class(request.POST, instance=lote)
        if  estatus_solicitud == 2:
            disponibilidad = True
        else:
            disponibilidad = lote.estatus_lote == 1
        if form.is_valid() and form2.is_valid() and disponibilidad:
            sol = Solicitud.objects.filter(lote_id=id_lote) \
                .update(aprobacion_director=False, estatus_solicitud=5, aprobacion_gerente=False)
            form.save()
            form2.save()
            return redirect('pagos', *args, **kwargs)
#            return HttpResponseRedirect(self.get_success_url()) 
        else:
            return render(request, 'core/error.html', {'form': form})
'''
class estado_cuenta(ListView):
    template_name = 'finanzas/estado_cuenta.html'
    def get_context_data(self, **kwargs):
        context = super(estado_cuenta, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        pagos = Pago.objects.filter(convenio=pk).order_by('numero_pago')
        solicitud = Solicitud.objects.filter(id=pk).first()
        field_object = Solicitud._meta.get_field('precio_final')
        precio_final = field_object.value_from_object(solicitud)
        field_object = Solicitud._meta.get_field('enganche')
        enganche = field_object.value_from_object(solicitud)
        impPorPagar = precio_final - enganche
        context['impPorPagar'] = impPorPagar
        field_object = Solicitud._meta.get_field('cantidad_pagos')
        cantidad_pagos = field_object.value_from_object(solicitud)
        field_object = Solicitud._meta.get_field('pagos_pagados')
        pagos_pagados = field_object.value_from_object(solicitud)
        pagosPorPagar = cantidad_pagos - pagos_pagados
        context['pagosPorPagar'] = pagosPorPagar
        field_object = Solicitud._meta.get_field('importe_pagado')
        importe_pagado = field_object.value_from_object(solicitud)
        saldo = impPorPagar - importe_pagado
        context['pagosPorPagar'] = pagosPorPagar
        context['saldo'] = saldo
        context['solicitud'] = solicitud
        context['pagos'] = pagos
        context['id'] = pk
        context['menu'] = "pagar"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context["proyecto_tb"] = proyecto_tb
        context['num_proyecto'] = num_proyecto
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Estado de cuenta
        des_permiso = '_estado_cuenta'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Imprimir estado cuenta
        des_permiso = '_imp_estado_cuenta'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Actualizar mensualidad
        des_permiso = '_cap_dep_mensual'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk',0)
        queryset = Pago.objects.filter(convenio=pk)
        return queryset

class mod_pago(UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'finanzas/nvo_pago.html'
    def get_context_data(self, **kwargs):
        context = super(mod_pago, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
        permiso_str = 'nom_proy' + '_' + 'acceso'
        acceso = self.request.user.has_perms([permiso_str])
        context["proyecto_tb"] = proyecto_tb
        pk = self.kwargs.get('pk',0)
        tabla1 = Pago.objects.filter(id=pk)
        context['tabla1'] = tabla1
        fecha1 = str(tabla1[0].fecha_voucher)
        sol = self.kwargs.get('sol',0)
        context['sol'] = sol
        context['pk'] = pk
        context['fecha1'] = fecha1
        context['num_proyecto'] = num_proyecto
# Captura comprobante mensual
        des_permiso = '_cap_dep_mensual'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Confirmar comprobante mensual
        des_permiso = '_confirma_deposito_mensual'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk',0)
        pago1 = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=pago1)
        if form.is_valid():
            pago_guardado = form.save()
            sol = self.kwargs.get('sol',0)
#            pag_act = Pago.objects.filter(id=pk).update(estatus_pago=2)
            total_pagado = Pago.objects.filter(convenio=sol,estatus_pago=2).values('convenio'). \
                annotate(pagos_pagados=Count('importe_pagado'),importe_pagado=Sum('importe_pagado'))
            if total_pagado:
                pagos_pagados = total_pagado[0]['pagos_pagados']
                importe_pagado = total_pagado[0]['importe_pagado']
            else:
                pagos_pagados = 0
                importe_pagado = 0

            sol_act = Solicitud.objects.filter(id=sol). \
                update(pagos_pagados=pagos_pagados, importe_pagado=importe_pagado)
#        return reverse_lazy(self.get_context_data(form=form))
        return HttpResponseRedirect(self.get_success_url())
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('sol',0)
        return reverse_lazy('estado_cuenta', kwargs={'pk':pk, 'num_proyecto': num_proyecto})

class estado_cuenta_PDF(View):
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
        context = {}
        template = get_template('finanzas/estado_cuenta_PDF.html')
        pk = self.kwargs['pk']
        datos = Pago.objects.filter(convenio=pk).order_by('numero_pago')
        total_por_pagar = Pago.objects.filter(convenio=pk).values('convenio'). \
            annotate(cantidad=Count('numero_pago'),suma=Sum('importe'))
        total_pagado = Pago.objects.filter(convenio=pk, importe_pagado__gt=0).values('convenio'). \
            annotate(cantidad=Count('numero_pago'),suma=Sum('importe'))
        solicitud = Solicitud.objects.filter(id=pk)
        titulo = Titulo.objects.filter(id=1)
        hoy = fecha_hoy()
        empresa = trae_empresa(1)
        context['solicitud'] = solicitud
        context['datos'] = datos
        context['menu'] = "solicitud"
        context['hoy'] = hoy
        context['pk'] = pk
        context['titulo'] = titulo
        pagado = 0
        importe_pagado = 0
        if total_pagado:
            pagado = total_pagado[0]['cantidad']
            importe_pagado = total_pagado[0]['suma']
        por_pagar = total_por_pagar[0]['cantidad']
        importe_por_pagar = total_por_pagar[0]['suma']
        pagos_saldo = por_pagar - pagado
        importe_saldo = importe_por_pagar - importe_pagado
        context['por_pagar'] = por_pagar
        context['importe_por_pagar'] = importe_por_pagar
        context['pagado'] = pagado
        context['importe_pagado'] = importe_pagado
        context['pagos_saldo'] = pagos_saldo
        context['importe_saldo'] = importe_saldo

        
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, 
            dest=response,
            link_callback=self.link_callback,
        )
        return response

class lista_pagos_PDF(View):
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
        num_proyecto = self.kwargs['num_proyecto']
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
    #  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
    # Listado contratos
        des_permiso = '_imprime_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = request.user.has_perms([permiso_str])
        if acceso:
            context = {}
            template = get_template('finanzas/listado_pagos_PDF.html')
            pk = self.kwargs['pk']
            datos = Pago.objects.filter(convenio=pk).order_by('numero_pago')
            total_por_pagar = Pago.objects.filter(convenio=pk).values('convenio'). \
                annotate(cantidad=Count('numero_pago'),suma=Sum('importe'))
            total_pagado = Pago.objects.filter(convenio=pk, importe_pagado__gt=0).values('convenio'). \
                annotate(cantidad=Count('numero_pago'),suma=Sum('importe'))
            solicitud = Solicitud.objects.filter(id=pk)
            titulo = Titulo.objects.filter(id=1)
            hoy = fecha_hoy()
            empresa = trae_empresa(1)
            context['solicitud'] = solicitud
            context['datos'] = datos
            context['menu'] = "solicitud"
            context['hoy'] = hoy
            context['pk'] = pk
            context['titulo'] = titulo

            por_pagar = total_por_pagar[0]['cantidad']
            importe_por_pagar = total_por_pagar[0]['suma']
            if total_pagado:
                pagado = total_pagado[0]['cantidad']
                importe_pagado = total_pagado[0]['suma']
            else:
                pagado = 0
                importe_pagado = 0
            pagos_saldo = por_pagar - pagado
            importe_saldo = importe_por_pagar - importe_pagado

            context['por_pagar'] = por_pagar
            context['importe_por_pagar'] = importe_por_pagar
            context['pagado'] = pagado
            context['importe_pagado'] = importe_pagado
            context['pagos_saldo'] = pagos_saldo
            context['importe_saldo'] = importe_saldo

            
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=self.link_callback,
            )
        return response

class contrato_contado(ListView):
    template_name = 'finanzas/contrato_contado.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])        
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(contrato_contado, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        asigna_solicitud = f_asigna_solicitud(self)
        if asigna_solicitud:
            totales = Solicitud.objects \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        else:
            id_empleado = f_empleado(self)
            totales = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))

        if 'totales' not in context:
            context['totales'] = totales
        if 'menu' not in context:
            context['menu'] = "contado"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado de créditos
        des_permiso = '_contados'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
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

class contrato_credito(ListView):
    template_name = 'finanzas/contrato_credito.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        return queryset

    def get_context_data(self, **kwargs):
        asigna_solicitud = f_asigna_solicitud(self)
        context = super(contrato_credito, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        else:
            id_empleado = f_empleado(self)
            totales = Solicitud.objects.filter(asesor_id=id_empleado,lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        if 'totales' not in context:
            context['totales'] = totales
        if 'menu' not in context:
            context['menu'] = "credito"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado de créditos
        des_permiso = '_creditos'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
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
