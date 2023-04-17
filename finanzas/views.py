import os
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from datetime import date
from django.conf import settings
#from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, View
from django.template.loader import get_template
from django.http.response import HttpResponse, HttpResponseRedirect
from time import gmtime, strftime
from xhtml2pdf import pisa
from django.db.models import Subquery, Sum, F, Q
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.db.models.aggregates import Count
from django.core.files import File
from django.shortcuts import render, get_object_or_404

from django.test import RequestFactory

from bien.models import PagoComision, Proyecto, Lote
from core.models import STATUS_COMISION, Titulo
from core.numero_letras import numero_a_letras
from empleado.models import Empleado
from .funciones import datos_comision_detalle, datos_comision_detalle_concentrado, datos_comisiones_concentrado, datos_tabla_amortizacion, fecha_periodo
from core.funciones import datos_fecha, fecha_hoy, fecha_hoy_amd, fecha_hoy_d, fecha_inicio_dia_mes_pago, fecha_to_str_amd, fecha_ultima_pago, fecha_ultimo_dia_mes, fecha_ultimo_dia_mes_pago, str_to_fecha_amd, str_to_fecha_dma, str_to_str_cambiar, suma_dias_fecha, trae_empresa
from gestion.models import Folios, Solicitud
from gestion.funciones import f_area_puesto, f_asigna_solicitud, f_empleado, nuevo_folio
from finanzas.models import Pago
from .forms import PagoForm, ComprobanteForm, Comprobante_MensualidadForm
from django.db import transaction

def elimina_archivo_url(request, almacen, id, documento, pk, num_proyecto):
    if almacen == 'Solicitud' or almacen == 'Pago':
        if almacen == 'Solicitud':
            pdf = get_object_or_404(Solicitud, pk=id)
        elif almacen == 'Pago':
            pdf = get_object_or_404(Pago, pk=id)
        setattr(pdf, documento, '')
        pdf.save()
        factory = RequestFactory()
        response = comprobantes.as_view()(request, pk=pk, num_proyecto=num_proyecto)
        return response
    else:
        return JsonResponse({'mensaje': 'Error'})

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

def archiva_credito(request, pk, num_proyecto):
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_archivar_credito'
    variable_proy = nom_proy + des_permiso
    permiso_str = "finanzas." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        archiva_solicitud = Solicitud.objects.filter(id=pk).update(estatus_solicitud = 7)
        
    return HttpResponseRedirect(reverse_lazy(('pagar'), kwargs={'num_proyecto':num_proyecto} ,))

class pagar(ListView):
    model = Solicitud
    template_name = 'finanzas/pagar.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#                .annotate(para_pagar=F('precio_final') - F('enganche')).filter(para_pagar__gt=F('importe_pagado')) \
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(estatus_solicitud=10) 
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud=10) 
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud=10) 
        elif datos['area_operativa'] == 2:
            # Finanzas
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud = 10) 
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .filter(estatus_solicitud=10) 
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)


#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .filter(estatus_solicitud=10) 
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor_id=id_empleado) \
#                .filter(estatus_solicitud=10) 
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
#  Archiva crédito
        des_permiso = '_archiva_credito'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
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
# imprime recibo mensual
        des_permiso = '_imprime_comprob_mensual'
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
        context['importe'] = tabla1[0].importe
        context['importe_pagado'] = tabla1[0].importe_pagado
        context['cuenta'] = tabla1[0].cuenta
        context['numero_comprobante'] = tabla1[0].numero_comprobante
        context['pagado_vencido'] = tabla1[0].pagado_vencido
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
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('sol',0)
        return reverse_lazy('estado_cuenta', kwargs={'pk':pk, 'num_proyecto': num_proyecto})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = self.kwargs.get('pk',0)
        pago1 = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=pago1)
        fecha_pago = request.POST.get('fecha_pago')
        importe_pagado = request.POST.get('importe_pagado').replace(',','')
        importe = request.POST.get('importe').replace(',','')
        deposito = request.POST.get('deposito')
        forma_pago = request.POST.get('forma_pago')
        cuenta = request.POST.get('cuenta')
        numero_comprobante = request.POST.get('numero_comprobante')
        estatus_pago = request.POST.get('estatus_pago')
        file_comprobante = request.POST.get('file_comprobante')
        fecha_voucher = request.POST.get('fecha_voucher')
        pagado_vencido = request.POST.get('pagado_vencido')


        data = {
            'fecha_pago': fecha_pago,
            'importe': importe,
            'importe_pagado': importe_pagado,
            'deposito': deposito,
            'forma_pago': forma_pago,
            'cuenta': cuenta,
            'numero_comprobante': numero_comprobante,
            'estatus_pago': estatus_pago,
            'file_comprobante': file_comprobante,
            'fecha_voucher': fecha_voucher,
            'pagado_vencido': pagado_vencido,
        }
#        valida = True
#        if form.errors:
#            for field in form:
#                for error in field.errors:
#                    if error != "Introduzca un número.":
#                        valida = False
#        if form.is_valid():
        mensualidad_valida = self.form_class(data)
        if mensualidad_valida.is_valid():
            with transaction.atomic():
#                pago_guardado = form.save()
                if deposito == '2':
                    estatus_pago = 2 
                mensualidad_upd = Pago.objects.get(id=pk)
                mensualidad_upd.importe_pagado = importe_pagado
                mensualidad_upd.deposito = deposito
                mensualidad_upd.forma_pago = forma_pago
                mensualidad_upd.cuenta = cuenta
                mensualidad_upd.numero_comprobante = numero_comprobante
                mensualidad_upd.estatus_pago = estatus_pago
                mensualidad_upd.file_comprobante = file_comprobante
                mensualidad_upd.fecha_voucher = fecha_voucher
                mensualidad_upd.pagado_vencido = pagado_vencido
                mensualidad_upd.save()
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
                pago_actual = Pago.objects.filter(id=pk)
                if pago_actual:
                    folio = pago_actual[0].folio_recibo
                    confirmado = pago_actual[0].deposito
                    importe_pagado = pago_actual[0].importe_pagado
                    if folio == 0 and confirmado == 2:
                        folio_recibo = nuevo_folio(6)
                        cantidad_pagos = pago_actual[0].convenio.cantidad_pagos
                        lote = pago_actual[0].convenio.lote.identificador_bien
                        nom_proyecto = pago_actual[0].convenio.lote.proyecto.nom_proyecto
                        observacion = "Pago mensual " + str(folio_recibo) + "/" + str(cantidad_pagos) + \
                            " del bien " + lote + " del proyecto " + nom_proyecto
                        folio = Folios(
                            tipo = 6, 
                            numero = folio_recibo,
                            observacion = observacion,
                            importe = importe_pagado)
                        folio.save()
                        pago_nuevo_folio = Pago.objects.filter(id=pk). \
                            update(folio_recibo=folio_recibo)
            return HttpResponseRedirect(self.get_success_url())
        else:
#        return reverse_lazy(self.get_context_data(form=form))
            context = {}
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
            sol = self.kwargs.get('sol',0)
            context['fecha_pago'] = fecha_pago
            context['deposito'] = deposito
            context['forma_pago'] = forma_pago
            context['estatus_pago'] = estatus_pago
            context['file_comprobante'] = file_comprobante
            context['sol'] = sol
            context['pk'] = pk
            context['importe'] = importe
            context['importe_pagado'] = importe_pagado
            context['cuenta'] = cuenta
            context['numero_comprobante'] = numero_comprobante
            context['fecha1'] = fecha_voucher
            context['num_proyecto'] = num_proyecto
            context['pagado_vencido'] = pagado_vencido
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
            context["form"] = mensualidad_valida
            return render(self.request, self.template_name, context)

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
            annotate(cantidad=Count('numero_pago'),suma=Sum('importe_pagado'))
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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])        
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])        
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])        
        elif datos['area_operativa'] == 2:
            # Finanzas
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])        
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
                .filter(modo_pago__in=[1,3])
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)



#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
#                .filter(modo_pago__in=[1,3])        
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor_id=id_empleado) \
#                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,6,7,9])  \
#                .filter(modo_pago__in=[1,3])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(contrato_contado, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        asigna_solicitud = f_asigna_solicitud(self)
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            totales = Solicitud.objects \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            totales = Solicitud.objects \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            totales = Solicitud.objects \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif datos['area_operativa'] == 2:
            # Finanzas
            totales = Solicitud.objects \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            totales = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        else:
            # SIN ACCESO
            totales = Solicitud.objects.filter(asesor_id=0)

#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            totales = Solicitud.objects \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
#                .aggregate(contratos=Count('id',distinct=True) \
#                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
#                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
#        else:
#            id_empleado = f_empleado(self)
#            totales = Solicitud.objects.filter(asesor_id=id_empleado) \
#                .filter(estatus_solicitud__in=[2,3,6,7,9], modo_pago__in=[1,3],lote__in=Subquery(lotes.values('pk'))) \
#                .aggregate(contratos=Count('id',distinct=True) \
#                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
#                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))

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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        elif datos['area_operativa'] == 2:
            # Finanzas
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado) \
                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
                .filter(modo_pago__in=[2,4])        
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)

#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
#                .filter(modo_pago__in=[2,4])        
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor_id=id_empleado) \
#                .order_by('num_contrato').filter(estatus_solicitud__in=[2,3,4,6,7,10])  \
#                .filter(modo_pago__in=[2,4])        
        return queryset

    def get_context_data(self, **kwargs):
        asigna_solicitud = f_asigna_solicitud(self)
        context = super(contrato_credito, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif datos['area_operativa'] == 2:
            # Finanzas
            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            totales = Solicitud.objects.filter(asesor_id=id_empleado,lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
                .aggregate(contratos=Count('id',distinct=True) \
                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
        else:
            # SIN ACCESO
            totales = Solicitud.objects.filter(asesor_id=0)


#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            totales = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
#                .aggregate(contratos=Count('id',distinct=True) \
#                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
#                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))
#        else:
#            id_empleado = f_empleado(self)
#            totales = Solicitud.objects.filter(asesor_id=id_empleado,lote__in=Subquery(lotes.values('pk'))) \
#                .filter(estatus_solicitud__in=[2,3,4,6,7,10], modo_pago__in=[2,4]) \
#                .aggregate(contratos=Count('id',distinct=True) \
#                    ,ventas=Sum('precio_final'), pagado=Sum('apartado') + Sum('pago_adicional') + Sum('importe_pagado') \
#                    ,por_pagar=Sum('precio_final') - Sum('apartado') - Sum('pago_adicional') - Sum('importe_pagado'))

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

class detalle_comisiones(LoginRequiredMixin, ListView):
    template_name = 'finanzas/detalle_comisiones.html'  
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(detalle_comisiones, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        fecha_desde_str = self.kwargs.get('fecha_desde')
        fecha_hasta_str = self.kwargs.get('fecha_hasta')
        grupo = self.kwargs.get('grupo',0)
        estatus_comision = self.kwargs.get('estatus_comision',0)
        periodo = self.kwargs.get('periodo',0)
        context['periodo'] = periodo
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        grupo = self.kwargs.get('grupo',0)
        context['grupo'] = grupo
        fecha_desde = date(int(fecha_desde_str[0:4]), int(fecha_desde_str[5:7]), int(fecha_desde_str[8:10]))
        fecha_hasta = date(int(fecha_hasta_str[0:4]), int(fecha_hasta_str[5:7]), int(fecha_hasta_str[8:10]))
        context['fecha_desde'] = fecha_desde
        context['fecha_hasta'] = fecha_hasta
        datos = datos_comision_detalle(grupo, num_proyecto, fecha_desde, fecha_hasta, estatus_comision, pk, periodo)
        if grupo == '1':
            nombre = datos[0].asesor_pago.nombre_completo
        elif grupo == '2':
            nombre = datos[0].gerente_pago.nombre_completo
        else:
            nombre = 'Publicidad'
        context['nombre'] = nombre
        cantidad = 0
        importe = 0
        if datos:
            for d in datos:
                cantidad += 1
                if grupo == '1':
                    importe += d.importe
                elif grupo == '2':
                    importe += d.importe_gerente
                else:
                    importe += d.importe_publicidad
        context['importe'] = importe
        context['cantidad'] = cantidad


        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk',0)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        fecha_hasta_str = self.kwargs.get('fecha_hasta')
        fecha_hasta = date(int(fecha_hasta_str[0:4]), int(fecha_hasta_str[5:7]), int(fecha_hasta_str[8:10]))
        fecha_desde_str = self.kwargs.get('fecha_desde')
        fecha_hasta_str = self.kwargs.get('fecha_hasta')
        fecha_desde = date(int(fecha_desde_str[0:4]), int(fecha_desde_str[5:7]), int(fecha_desde_str[8:10]))
        fecha_hasta = date(int(fecha_hasta_str[0:4]), int(fecha_hasta_str[5:7]), int(fecha_hasta_str[8:10]))
        grupo = self.kwargs.get('grupo',0)
        periodo = self.kwargs.get('periodo',0)
        estatus_comision = self.kwargs.get('estatus_comision',0)
        queryset = datos_comision_detalle(grupo, num_proyecto, fecha_desde, fecha_hasta, estatus_comision, pk, periodo)
#        if grupo == "1":
#            queryset = PagoComision.objects \
#                .filter(fecha_contrato__range=[fecha_desde_p, fecha_hasta_p], \
#                    proyecto_pago=num_proyecto, estatus_comision=0, asesor_pago=pk) \
#                .order_by('-fecha_contrato') 
#        else:
#            queryset = PagoComision.objects \
#                .filter(fecha_contrato__range=[fecha_desde_p, fecha_hasta_p], \
#                    proyecto_pago=num_proyecto, estatus_comision=0) \
#                .order_by('gerente_pago','-fecha_contrato') 
        return queryset

class pago_comisiones(LoginRequiredMixin, ListView):
    template_name = 'finanzas/pago_comisiones.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(pago_comisiones, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
# Si tiene permisos para comisiones
        nom_proy = proyecto_tb[0].nom_proy

        permiso_str = "finanzas." + nom_proy + '_' + 'pago_normal_comisiones'
        acceso = self.request.user.has_perms([permiso_str])
        context['app_proy_pago_normal_comisiones'] = acceso

        permiso_str = "finanzas." + nom_proy + '_' + 'vobo_comisiones'
        acceso = self.request.user.has_perms([permiso_str])
        context['app_proy_vobo_comisiones'] = acceso

        permiso_str = "bien." + nom_proy + '_' + 'imprime_comprob_comision'
        acceso = self.request.user.has_perms([permiso_str])
        context['app_proy_imprime_comprob_comision'] = acceso

        context['proyecto_tb'] = proyecto_tb
        datos = datos_fecha(num_proyecto)
        context['datos'] = datos
#  -----------------
#  Actualización de pantallas
#  -----------------
# Información viene del template
        fecha_hasta_cmb = fecha_periodo(self)
# FIN FECHA SELECCIONADA
        periodo = fecha_to_str_amd(fecha_hasta_cmb)
        fecha_desde_p = fecha_inicio_dia_mes_pago(fecha_hasta_cmb)
        fecha_hasta_p = fecha_ultimo_dia_mes_pago(fecha_hasta_cmb)

        context['fecha_desde'] = fecha_desde_p
        context['fecha_hasta'] = fecha_hasta_p
        context['periodo'] = periodo
    
        pagos_pagados = PagoComision.objects.filter(fecha_periodo=periodo, proyecto_pago=num_proyecto)
        if pagos_pagados:
            estatus_comision = pagos_pagados[0].estatus_comision
#            pago_comision = datos_comision_detalle_concentrado(1, num_proyecto, fecha_desde_p, fecha_hasta, estatus_comision)
            pago_comision_detalle = datos_comisiones_concentrado(num_proyecto, periodo, periodo, estatus_comision)
            pagos_gerentes = datos_comision_detalle_concentrado(2, num_proyecto, periodo, periodo, estatus_comision)
            acumulados = datos_comisiones_concentrado(num_proyecto, periodo, periodo, estatus_comision)
        else:
            estatus_comision = 0
#            pago_comision = datos_comision_detalle_concentrado(1, num_proyecto, fecha_desde_p, fecha_hasta_p, estatus_comision)
            pago_comision_detalle = datos_comisiones_concentrado(num_proyecto, fecha_desde_p, fecha_hasta_p, estatus_comision)
            pagos_gerentes = datos_comision_detalle_concentrado(2,num_proyecto, fecha_desde_p, fecha_hasta_p, estatus_comision)
            acumulados = datos_comisiones_concentrado(num_proyecto, fecha_desde_p, fecha_hasta_p, estatus_comision)
        context['pago_comision_detalle'] = pago_comision_detalle
        if acumulados:
            importe_asesores = acumulados[0]['total_asesor']
            importe_gerente = acumulados[0]['total_gerente']
            importe_publicidad = acumulados[0]['total_publicidad']
            estatus_pago_publicidad = acumulados[0]['estatus_pago_publicidad']
            importe_general = importe_asesores + importe_gerente + importe_publicidad
            bienes_publicidad = acumulados[0]['bienes']
            folio_comision_publicidad = acumulados[0]['folio_comision_publicidad']
        else:
            importe_asesores = 0
            importe_gerente = 0
            importe_publicidad = 0
            importe_general = 0
            estatus_pago_publicidad = 0
            bienes_publicidad = 0
            folio_comision_publicidad = 0
        texto_estatus = STATUS_COMISION[estatus_comision][1]
        context['texto_estatus'] = texto_estatus
        context['estatus_pago_publicidad'] = estatus_pago_publicidad
        context['estatus_comision'] = estatus_comision
        context['importe_asesores'] = importe_asesores
        context['importe_gerente'] = importe_gerente
        context['importe_publicidad'] = importe_publicidad
        context['importe_general'] = importe_general
        context['bienes_publicidad'] = bienes_publicidad
        context['folio_comision_publicidad'] = folio_comision_publicidad

        context['pagos_gerentes'] = pagos_gerentes
        return context
    def get_queryset(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        fecha_hasta = fecha_periodo(self)
        periodo = fecha_hasta
        fecha_desde_p = fecha_inicio_dia_mes_pago(fecha_hasta)
        fecha_hasta_p = fecha_ultimo_dia_mes_pago(fecha_hasta)
        pagos_pagados = PagoComision.objects.filter(fecha_periodo=fecha_hasta,proyecto_pago=num_proyecto)
        if pagos_pagados:
            estatus_comision = pagos_pagados[0].estatus_comision
            queryset = datos_comision_detalle_concentrado(1, num_proyecto, fecha_hasta, fecha_hasta_p, estatus_comision)
        else:
            estatus_comision = 0
            queryset = datos_comision_detalle_concentrado(1, num_proyecto, fecha_desde_p, fecha_hasta_p, estatus_comision)
        return queryset
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return self.reverse_lazy(self.get_context_data(form=form))

def deposito_comision(self, fecha, num_proyecto, empleado, opcion):
    fecha_hasta = fecha
    hoy = fecha_hoy_amd()
    if opcion == '1':
#  Asesor
        pago_comision_detalle = PagoComision.objects \
            .filter(fecha_periodo=fecha_hasta, proyecto_pago=num_proyecto, \
                asesor_pago_id=empleado).update(estatus_pago_asesor=1,fecha_deposito_comision=hoy)
    elif opcion== '2':
#  Gerente
        pago_comision_detalle = PagoComision.objects \
            .filter(fecha_periodo=fecha_hasta, proyecto_pago=num_proyecto, \
            gerente_pago_id=empleado).update(estatus_pago_gerente=1,fecha_deposito_comision_gerente=hoy)
    elif opcion== '3':
#  Publicidad
        pago_comision_detalle = PagoComision.objects \
            .filter(fecha_periodo=fecha_hasta, proyecto_pago=num_proyecto) \
            .update(estatus_pago_publicidad=1,fecha_deposito_comision_publicidad=hoy)
    confirma = PagoComision.objects \
        .filter(fecha_periodo=fecha_hasta, proyecto_pago=num_proyecto)
    confirmado = 1
    for c in confirma:
        if c.estatus_pago_asesor == 0:
            confirmado = 0
        if c.estatus_pago_gerente == 0:
            confirmado = 0
        if c.estatus_pago_publicidad == 0:
            confirmado = 0
    if confirmado == 1:
        deposito_confirmado = PagoComision.objects \
            .filter(fecha_periodo=fecha_hasta, proyecto_pago=num_proyecto) \
            .update(estatus_comision=2)
    return HttpResponseRedirect(reverse_lazy(('pago_comisiones'), kwargs={'num_proyecto':num_proyecto,'periodo':fecha} ,))

class situacion_comisiones(LoginRequiredMixin, ListView):
    template_name = 'finanzas/situacion_comisiones.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_context_data(self, **kwargs):
        context = super(situacion_comisiones, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        nom_proy = proyecto_tb[0].nom_proy
        permiso_str = "finanzas." + nom_proy + '_consulta_comisiones'
        acceso = self.request.user.has_perms([permiso_str])
        context['app_proy_consulta_comisiones'] = acceso
        nombre = proyecto_tb[0].nombre
        context['nombre'] = nombre
        return context
    def get_queryset(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        queryset = PagoComision.objects.filter(proyecto_pago=num_proyecto) 
        return queryset

def vobo_comisiones(request, fecha_hasta_str, num_proyecto, fecha_hasta, nom_proyecto, imp_ger, imp_pub):
    fecha_hasta1 = str_to_fecha_amd(fecha_hasta)
    fecha_desde_p = fecha_inicio_dia_mes_pago(fecha_hasta1)
    fecha_hasta_p = fecha_ultimo_dia_mes_pago(fecha_hasta1)
#   Vobo a todos los registros asesor con gerente y director publicidad y folio publicidad
    pago_comision_detalle = PagoComision.objects \
        .filter(fecha_contrato__range=[fecha_desde_p, fecha_hasta_p], \
            proyecto_pago=num_proyecto) \
        .update(estatus_comision=1, \
            fecha_periodo=fecha_hasta_str)
#   Folio de publicidad
    importe_publicidad = imp_pub.replace(",","").replace(",","")
    folio_publicidad = nuevo_folio(3)
    observacion = "Comisión publicidad de fecha " + fecha_hasta_str + \
        " del proyecto " + nom_proyecto
    folio = Folios(
        tipo = 3, 
        numero = folio_publicidad,
        observacion = observacion,
        importe = importe_publicidad)
    folio.save()
#   Actualiza folio publicidad    
    act_folio_publicidad = PagoComision.objects \
        .filter(proyecto_pago=num_proyecto, \
            fecha_periodo=fecha_hasta_str) \
        .update(folio_comision_publicidad=folio_publicidad,)
    pago_comision_gerente_detalle = PagoComision.objects \
        .filter(proyecto_pago=num_proyecto, \
            fecha_periodo=fecha_hasta_str) \
        .order_by('gerente_pago')
    gerente_ant = 0
    suma_gerente = 0
    for pago in pago_comision_gerente_detalle:
        num_gerente = pago.gerente_pago
        if num_gerente != gerente_ant:
            if gerente_ant == 0:
                suma_gerente += pago.importe_gerente
                nombre = pago.gerente_pago.nombre_completo
                gerente_ant = num_gerente
                bien = pago.bien_pago
                folio_gerente = nuevo_folio(3)
                actualiza = PagoComision.objects \
                    .filter(bien_pago=pago.bien_pago) \
                    .update(folio_comision_gerente=folio_gerente,)
            else:
                observacion = "Comisión gerente de fecha " + fecha_hasta_str + \
                    " del proyecto " + nom_proyecto + " para  " + nombre
                folio = Folios(
                    tipo = 3, 
                    numero = folio_gerente,
                    observacion = observacion,
                    importe = suma_gerente)
                folio.save()
                suma_gerente = pago.importe_gerente
                gerente_ant = pago.gerente_pago
                nombre = pago.gerente_pago.nombre_completo
                bien = pago.bien_pago
                folio_gerente = nuevo_folio(3)
                actualiza = PagoComision.objects \
                    .filter(bien_pago=pago.bien_pago) \
                    .update(folio_comision_gerente=folio_gerente,)
        else:
            bien = pago.bien_pago
            actualiza = PagoComision.objects \
                .filter(bien_pago=pago.bien_pago) \
                .update(folio_comision_gerente=folio_gerente,)
            suma_gerente += pago.importe_gerente
    if suma_gerente > 0:
        observacion = "Comisión gerente de fecha " + fecha_hasta_str + \
            " del proyecto " + nom_proyecto + " para  " + nombre
        folio = Folios(
            tipo = 3, 
            numero = folio_gerente,
            observacion = observacion,
            importe = suma_gerente)
        folio.save()
    empleado_ant = 0
    pago_comision_detalle = PagoComision.objects \
        .filter(fecha_contrato__range=[fecha_desde_p, fecha_hasta_p], proyecto_pago=num_proyecto) \
        .order_by('asesor_pago')
    for pago in pago_comision_detalle:
        if not pago.asesor_pago == empleado_ant:
            if empleado_ant == 0:
                suma_asesor = pago.importe
                empleado_ant = pago.asesor_pago
                nombre = pago.asesor_pago.nombre_completo
                bien = pago.bien_pago
                folio_asesor = nuevo_folio(3)
                actualiza = PagoComision.objects \
                    .filter(bien_pago=bien) \
                    .update(folio_comision_asesor=folio_asesor)
            else:
                observacion = "Comisión agente " + nombre + \
                    " de fecha " + fecha_hasta_str + " del proyecto " + nom_proyecto
                folio = Folios(
                    tipo = 3, 
                    numero = folio_asesor,
                    observacion = observacion,
                    importe = suma_asesor)
                folio.save()
                empleado_ant = pago.asesor_pago
                suma_asesor = pago.importe
                bien = pago.bien_pago
                nombre = pago.asesor_pago.nombre_completo
                folio_asesor = nuevo_folio(3)
                actualiza = PagoComision.objects \
                    .filter(bien_pago=bien) \
                    .update(folio_comision_asesor=folio_asesor)
        else:
            bien = pago.bien_pago
            actualiza = PagoComision.objects \
                .filter(bien_pago=bien) \
                .update(folio_comision_asesor=folio_asesor)
            suma_asesor += pago.importe
    if suma_asesor > 0:
        observacion = "Comisión agente " + nombre + \
            " de fecha " + fecha_hasta_str + " del proyecto " + nom_proyecto
        folio = Folios(
            tipo = 3, 
            numero = folio_asesor,
            observacion = observacion,
            importe = suma_asesor)
        folio.save()
    return HttpResponseRedirect(reverse_lazy(('pago_comisiones'), kwargs={'num_proyecto':num_proyecto,'periodo':fecha_hasta_str} ,))

class imprime_comprob_mensual_PDF(LoginRequiredMixin, View):
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
        des_permiso = '_imprime_comprob_mensual'
        num_proyecto = self.kwargs['num_proyecto']
        proyecto = Proyecto.objects.filter(id=num_proyecto)
        nom_proy = proyecto[0].nom_proy
        variable_proy = nom_proy + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = request.user.has_perms([permiso_str])
        if acceso:
            pk = self.kwargs['pk']
            pago = Pago.objects.filter(id=pk)
            context = {}
            template = get_template('finanzas/recibo_pago_mensualidadPDF.html')
            hoy = fecha_hoy()
            empresa = trae_empresa(1)
            context['empresa'] = empresa
            context['proyecto'] = proyecto[0].nombre
            folio_recibo = pago[0].folio_recibo
            context['folio_recibo'] = folio_recibo
            context['hoy'] = hoy
            folio = Folios.objects.filter(tipo=6,numero=folio_recibo)
            concepto = folio[0].observacion
            importe = folio[0].importe
            context['concepto'] = concepto
            context['importe'] = importe
            centavos = "{:.2f}".format(round(importe, 2))[-2:]
            context['centavos'] = centavos
            importe_letras = numero_a_letras(importe)
            context['importe_letras'] = importe_letras
            copias = [0,1]
            context['copias'] = copias
            cliente_nombre = pago[0].convenio.cliente.cliente_nombre
            context['cliente_nombre'] = cliente_nombre
            
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=self.link_callback,
            )
        return response

class imprime_comprob_comision_PDF(LoginRequiredMixin, View):
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
        des_permiso = '_imprime_comprob_comision'
        num_proyecto = self.kwargs['num_proyecto']
        proyecto = Proyecto.objects.filter(id=num_proyecto)
        nom_proy = proyecto[0].nom_proy
        variable_proy = nom_proy + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = request.user.has_perms([permiso_str])
        response = HttpResponse(content_type='application/pdf', )
        if acceso:
            fecha = self.kwargs['fecha']
            empleado = self.kwargs['empleado']
            bienes = self.kwargs['bienes']
            importe = self.kwargs['importe']
            nom_proyecto = self.kwargs['nom_proyecto']
            folio = self.kwargs['folio']

            context = {}

            context['fecha'] = str_to_str_cambiar(fecha)
            context['empleado'] = empleado
            context['bienes'] = bienes
            context['importe'] = importe
            context['nom_proyecto'] = nom_proyecto
            context['folio'] = folio
            context['num_proyecto'] = num_proyecto


            template = get_template('finanzas/recibo_pago_comisionPDF.html')
            hoy = fecha_hoy()
            empresa = trae_empresa(1)
            context['empresa'] = empresa

            context['hoy'] = hoy

            importe_num = float(importe.replace(',','').replace(',',''))
            importe_letras = numero_a_letras(importe_num)
            context['importe_letras'] = importe_letras
            copias = [0,1]
            context['copias'] = copias
            
            html = template.render(context)
            pisaStatus = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=self.link_callback,
            )
        else:
            print('Sin acceso')
        return response

class comprobantes(LoginRequiredMixin, UpdateView):
    model = Solicitud
    form_class = ComprobanteForm
    template_name = 'finanzas/comprobantes.html'
    def get_context_data(self, **kwargs):
        context = super(comprobantes, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
        context['solicitud'] = Solicitud.objects.filter(id=pk)
        context['mensualidades'] = Pago.objects.filter(convenio=pk)
        context['id'] = pk
        context['pk'] = pk
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['nom_proyecto'] = proyecto_tb[0].nombre
        context['num_proyecto'] = num_proyecto
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Actualiza comprobantes
        des_permiso = '_cambia_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk',0)
        solicitud = Solicitud.objects.get(id=pk)
        guardar = False
        if 'foto_comprobante_apartado' in request.FILES:
            guardar = True
            solicitud.foto_comprobante_apartado = request.FILES['foto_comprobante_apartado']
        if 'recibo_firmado_apa' in request.FILES:
            guardar = True
            solicitud.recibo_firmado_apa = request.FILES['recibo_firmado_apa']
        if 'foto_comprobante_pago_adicional' in request.FILES:
            guardar = True
            solicitud.foto_comprobante_pago_adicional = request.FILES['foto_comprobante_pago_adicional']
        if 'recibo_firmado_pa' in request.FILES:
            guardar = True
            solicitud.recibo_firmado_pa = request.FILES['recibo_firmado_pa']
        if guardar:
            solicitud.save()
        comprobantes = request.FILES
        for comprobante in comprobantes:
            if comprobante.startswith('file-comprobante-'):
                partes = comprobante.split("-")
                registro = partes[2]
                pago = Pago.objects.get(id=registro)
                pago.file_comprobante = request.FILES[comprobante]
                pago.save()
            elif comprobante.startswith('recibo-firmado-'):
                partes = comprobante.split("-")
                registro = partes[2]
                pago = Pago.objects.get(id=registro)
                pago.recibo_firmado = request.FILES[comprobante]
                pago.save()        
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context = {}
    # Proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['num_proyecto'] = num_proyecto         
        context['proyecto_tb'] = proyecto_tb
        nom_proy = proyecto_tb[0].nom_proy
        nombre = proyecto_tb[0].nombre
        context['nombre'] = nombre
    # Solicitud
        formulario = Solicitud.objects.filter(id=pk)
        context['formulario'] = formulario
    # Pagos
        pago_tb = Pago.objects.filter(convenio_id=pk)
        context['pago_tb'] = pago_tb        
        return HttpResponseRedirect(reverse_lazy(('comprobantes'), kwargs={'pk': pk, 'num_proyecto':num_proyecto} ,))

