import os
import datetime
from django.db.models import Max, Q, Subquery
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import View
from django.template.loader import get_template
from time import gmtime, strftime
from requests import post
from xhtml2pdf import pisa
import numpy as np
from django.contrib.auth.decorators import login_required
from finanzas.models import Pago
from django.conf import settings
from django.contrib.staticfiles import finders
from django.views.generic.edit import ModelFormMixin
from django.db import transaction

from .models import *
from .funciones import *
from .forms import *
from core.numero_letras import numero_a_letras
from core.funciones import *

class solicitudes(ListView):
    model = Solicitud
    context_object_name = 'obj'
    template_name = 'gestion/solicitudes.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        num_proyecto = self.kwargs.get('num_proyecto')
        asigna_solicitud = f_asigna_solicitud(self)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        if asigna_solicitud:
            gerente = Empleado.objects.all().filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersdonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
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
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# ver listado solicitudes
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Agregar solicitud
        des_permiso = '_add_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cambiar solicitud
        des_permiso = '_cambia_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cancela solicitud
        des_permiso = '_cancela_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Listado amortizacion solicitud
        des_permiso = '_amortizacion'
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

@login_required
def guarda_cliente(request):
    id_cliente = request.POST.get('cliente')
    tipo_cliente = request.POST.get('tipo_cliente')
    razon = request.POST.get('razon')
    nombre = request.POST.get('nombre')
    paterno = request.POST.get('paterno')
    materno = request.POST.get('materno')
    nombre_conyuge = request.POST.get('nombre_conyuge')
    paterno_conyuge = request.POST.get('paterno_conyuge')
    materno_conyuge = request.POST.get('materno_conyuge')
    rfc = request.POST.get('rfc')
    curp = request.POST.get('curp')
    estado_civil = request.POST.get('estado_civil')
    regimen = request.POST.get('regimen')
    calle = request.POST.get('calle')
    colonia = request.POST.get('colonia')
    codpos = request.POST.get('codpos')
    municipio = request.POST.get('municipio')
    estado = request.POST.get('estado')
    celular = request.POST.get('celular')
    correo = request.POST.get('correo')
    upd_cliente = Cliente.objects.filter(id=id_cliente) \
        .update(tipo_cliente=tipo_cliente, razon=razon,nombre=nombre, \
        paterno=paterno, materno=materno, nombre_conyuge=nombre_conyuge, \
        paterno_conyuge=paterno_conyuge, materno_conyuge=materno_conyuge, \
        rfc=rfc, curp=curp, estado_civil=estado_civil, regimen=regimen, \
        calle=calle, colonia=colonia, codpos=codpos, municipio=municipio, \
        estado=estado, celular=celular, correo=correo)

class nva_solicitud(CreateView):
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
                query1 = Q(tipo_empleado='E', area_operativa=3) 
#                query2 = Q(id=f_emp)
#                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
                empleado_cmb = Empleado.objects.filter(query1)  \
                    .filter(subidPersdonal__in=Subquery(gerente.values('pk'))) \
                    .order_by('paterno','materno','nombre').all()
                context['f_emp'] = 0
            else:
                empleado_cmb = Empleado.objects.filter(id=f_emp) \
                    .order_by('paterno','materno','nombre')
                context['f_emp'] = f_emp
            context['empleado_cmb'] = empleado_cmb
#        context['form'] = self.form_class(self.request.GET)
        cliente_cmb = Cliente.objects.filter(estatus_cliente=1)
        context['cliente_cmb'] = cliente_cmb
        context['menu'] = "solicitud"
        context['accion'] = "Alta"
        context['sol'] = Solicitud.objects.filter(id = 0)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
        reglas = Regla.objects.filter(proyecto=num_proyecto)
        context['reglas'] = reglas
        for re in reglas:
            if re.modo_pago == 2:
                context['t_enganche_minimo'] = re.tipo_enganche_minimo
                context['v_enganche_minimo'] = re.valor3
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Agregar solicitud
        des_permiso = '_add_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cambiar solicitud
        des_permiso = '_cambia_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Asigna descuento solicitud
        des_permiso = '_asigna_descto'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        cliente = self.request.POST.get('cliente')
        if not cliente:
            asesor = 0
            lote = 0
            cliente = 0

            modo_pago = 1
            tipo_descuento = 0
            asigna_descuento = 0
            cantidad_pagos = 0

            precio_lote = 0
            precio_final = 0
            porcentaje_descuento = 0
            descuento = 0
            enganche = 0
            importe_x_pago = 0
            total = 0
            precio_x_mt = 0

            foto_elector_frente = " "
            foto_elector_reverso = ""
            foto_comprobante = " "
            foto_matrimonio = " "
            estatus_solicitud = 1
            foto_elector_frente_cy = " "
            foto_elector_reverso_cy = " "
            foto_alta_shcp = " "
            foto_acta_const = ""

            tipo_cliente = 0
            razon = " "
            nombre = " "
            paterno = " "
            materno = " "
            nombre_conyuge = " "
            paterno_conyuge = " "
            materno_conyuge = " "
            rfc = " "
            curp = " "
            estado_civil = 1
            regimen = 0
            calle = " "
            colonia = " "
            codpos = " "
            codpos = " "
            municipio = " "
            estado = 0
            celular = " "
            correo = ""
        else:
            asesor = self.request.POST.get('asesor_id')
            lote = self.request.POST.get('lote_id')
            cliente = self.request.POST.get('cliente_id')

            modo_pago = self.request.POST.get('modo_pago')
            tipo_descuento = self.request.POST.get('tipo_descuento')
            asigna_descuento = self.request.POST.get('asigna_descuento')
            cantidad_pagos = self.request.POST.get('cantidad_pagos')

            precio_lote = self.request.POST.get('precio_lote')
            precio_final = self.request.POST.get('precio_final')
            porcentaje_descuento = self.request.POST.get('porcentaje_descuento')
            descuento = self.request.POST.get('descuento')
            enganche = self.request.POST.get('enganche')
            importe_x_pago = self.request.POST.get('importe_x_pago')
            total = self.request.POST.get('total')
            precio_x_mt = self.request.POST.get('precio_x_mt')

            foto_elector_frente = self.request.POST.get('foto_elector_frente')
            foto_elector_reverso = self.request.POST.get('foto_elector_reverso')
            foto_comprobante = self.request.POST.get('foto_comprobante')
            foto_matrimonio = self.request.POST.get('foto_matrimonio')
            estatus_solicitud = self.request.POST.get('estatus_solicitud')
            foto_elector_frente_cy = self.request.POST.get('foto_elector_frente_cy')
            foto_elector_reverso_cy = self.request.POST.get('foto_elector_reverso_cy')
            foto_alta_shcp = self.request.POST.get('foto_alta_shcp')
            foto_acta_const = self.request.POST.get('foto_acta_const')
            tipo_cliente = self.request.POST.get('tipo_cliente')

            razon = self.request.POST.get('razon')
            nombre = self.request.POST.get('nombre')
            paterno = self.request.POST.get('paterno')
            materno = self.request.POST.get('materno')
            nombre_conyuge = self.request.POST.get('nombre_conyuge')
            paterno_conyuge = self.request.POST.get('paterno_conyuge')
            materno_conyuge = self.request.POST.get('materno_conyuge')
            rfc = self.request.POST.get('rfc')
            curp = self.request.POST.get('curp')
            
            estado_civil = self.request.POST.get('estado_civil')
            regimen = self.request.POST.get('regimen')
            calle = self.request.POST.get('calle')
            colonia = self.request.POST.get('colonia')
            codpos = self.request.POST.get('codpos')
            municipio = self.request.POST.get('municipio')
            estado = self.request.POST.get('estado')
            celular = self.request.POST.get('celular')
            correo = self.request.POST.get('correo')
        context["asesor"] = asesor
        context["lote"] = lote
        context["cliente"] = cliente

        context["modo_pago"] = modo_pago
        context["tipo_descuento"] = tipo_descuento
        context["asigna_descuento"] = asigna_descuento
        context["cantidad_pagos"] = cantidad_pagos

        context["precio_lote"] = precio_lote
        context["precio_final"] = precio_final
        context["porcentaje_descuento"] = porcentaje_descuento
        context["descuento"] = descuento
        context["enganche"] = enganche
        context["importe_x_pago"] = importe_x_pago

        context["foto_elector_frente"] = foto_elector_frente
        context["foto_elector_reverso"] = foto_elector_reverso
        context["foto_comprobante"] = foto_comprobante
        context["foto_matrimonio"] = foto_matrimonio
        context["estatus_solicitud"] = estatus_solicitud
        context["foto_elector_frente_cy"] = foto_elector_frente_cy
        context["foto_elector_reverso_cy"] = foto_elector_reverso_cy
        context["foto_alta_shcp"] = foto_alta_shcp
        context["foto_acta_const"] = foto_acta_const
        context["tipo_cliente"] = tipo_cliente

        context["razon"] = razon
        context["nombre"] = nombre
        context["paterno"] = paterno
        context["materno"] = materno
        context["nombre_conyuge"] = nombre_conyuge
        context["paterno_conyuge"] = paterno_conyuge
        context["materno_conyuge"] = materno_conyuge
        context["rfc"] = rfc
        context["curp"] = curp

        context["estado_civil"] = estado_civil
        context["regimen"] = regimen
        context["calle"] = calle
        context["colonia"] = colonia
        context["codpos"] = codpos
        context["municipio"] = municipio
        context["estado"] = estado
        context["celular"] = celular
        context["correo"] = correo
        return context
#    def get_success_url(self):
#        num_proyecto = self.kwargs.get('num_proyecto',0)
#        return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        
        num_proyecto = self.kwargs.get('num_proyecto',0)
        cliente = request.POST.get('cliente')
        asesor = request.POST.get('asesor')
        lote = request.POST.get('lote')

        modo_pago = int(request.POST.get('modo_pago').replace(',',''))
        tipo_descuento = int(request.POST.get('tipo_descuento').replace(',',''))
        asigna_descuento = request.POST.get('asigna_descuento')
        cantidad_pagos = request.POST.get('cantidad_pagos')

        precio_lote = request.POST.get('precio_lote').replace(',','')
        precio_final = request.POST.get('precio_final').replace(',','')
        porcentaje_descuento = request.POST.get('porcentaje_descuento').replace(',','')
        descuento = request.POST.get('descuento').replace(',','')
        enganche = request.POST.get('enganche').replace(',','')
        importe_x_pago = request.POST.get('importe_x_pago').replace(',','')
        total = request.POST.get('total').replace(',','')
        precio_x_mt = request.POST.get('precio_x_mt').replace(',','')

        foto_elector_frente = request.POST.get('foto_elector_frente')
        foto_elector_reverso = request.POST.get('foto_elector_reverso')
        foto_comprobante = request.POST.get('foto_comprobante')
        foto_matrimonio = request.POST.get('foto_matrimonio')
        estatus_solicitud = request.POST.get('estatus_solicitud')
        foto_elector_frente_cy = request.POST.get('foto_elector_frente_cy')
        foto_elector_reverso_cy = request.POST.get('foto_elector_reverso_cy')
        foto_alta_shcp = request.POST.get('foto_alta_shcp')
        foto_acta_const = request.POST.get('foto_acta_const')
        tipo_cliente = request.POST.get('tipo_cliente')

        razon = request.POST.get('razon')
        nombre = request.POST.get('nombre')
        paterno = request.POST.get('paterno')
        materno = request.POST.get('materno')
        nombre_conyuge = request.POST.get('nombre_conyuge')
        paterno_conyuge = request.POST.get('paterno_conyuge')
        materno_conyuge = request.POST.get('materno_conyuge')
        
        rfc = request.POST.get('rfc')
        curp = request.POST.get('curp')
        estado_civil = request.POST.get('estado_civil')
        regimen = request.POST.get('regimen')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        codpos = request.POST.get('codpos')
        municipio = request.POST.get('municipio')
        estado = request.POST.get('estado')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')

        data = {
            'cliente':cliente,
            'asesor':asesor,
            'lote':lote,
            'precio_lote':precio_lote,
            'precio_final':precio_final,
            'tipo_descuento':tipo_descuento,
            'asigna_descuento':asigna_descuento,
            'porcentaje_descuento':porcentaje_descuento,
            'descuento':descuento,
            'modo_pago':modo_pago,
            'enganche':enganche,
            'cantidad_pagos':cantidad_pagos,
            'importe_x_pago':importe_x_pago,
            'foto_elector_frente':foto_elector_frente,
            'foto_elector_reverso':foto_elector_reverso,
            'foto_comprobante':foto_comprobante,
            'foto_matrimonio':foto_matrimonio,
            'estatus_solicitud':estatus_solicitud,
            'foto_elector_frente_cy':foto_elector_frente_cy,
            'foto_elector_reverso_cy':foto_elector_reverso_cy,
            'foto_alta_shcp':foto_alta_shcp,
            'foto_acta_const':foto_acta_const,
            'tipo_cliente':tipo_cliente,
            'razon':razon,
            'nombre':nombre,
            'paterno':paterno,
            'materno':materno,
            'nombre_conyuge':nombre_conyuge,
            'paterno_conyuge':paterno_conyuge,
            'materno_conyuge':materno_conyuge,
            'rfc':rfc,
            'curp':curp,
            'estado_civil':estado_civil,
            'regimen':regimen,
            'calle':calle,
            'colonia':colonia,
            'codpos':codpos,
            'municipio':municipio,
            'estado':estado,
            'celular':celular,
            'correo':correo,
            'precio_x_mt':precio_x_mt,
            'total':total,
        }
        solicitud_valida = Nuvole_SolicitudForm(data)

        if solicitud_valida.is_valid():
            solicitud_valida.save()
            guarda_cliente(self.request)
#            return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
            return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto},))
        else:
            context = {}
            context['num_proyecto'] = num_proyecto
            context['lote_cmb'] = Lote.objects.filter(proyecto=num_proyecto,estatus_lote=1).all()
            if 'empleado_cmb' not in context:
                asigna_solicitud = f_asigna_solicitud(self)
                f_emp = f_empleado(self)
                if asigna_solicitud:
                    query1 = Q(tipo_empleado='E', area_operativa=3) 
    #                query2 = Q(id=f_emp)
    #                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                    gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
                    empleado_cmb = Empleado.objects.filter(query1)  \
                        .filter(subidPersdonal__in=Subquery(gerente.values('pk'))) \
                        .order_by('paterno','materno','nombre').all()
                    context['f_emp'] = 0
                else:
                    empleado_cmb = Empleado.objects.filter(id=f_emp) \
                        .order_by('paterno','materno','nombre')
                    context['f_emp'] = f_emp
                context['empleado_cmb'] = empleado_cmb
    #        context['form'] = self.form_class(self.request.GET)
            cliente_cmb = Cliente.objects.filter(estatus_cliente=1)
            context['cliente_cmb'] = cliente_cmb
            context['menu'] = "solicitud"
            context['accion'] = "Alta"
            context['sol'] = Solicitud.objects.filter(id = 0)
            proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
            context['proyecto_tb'] = proyecto_tb
            context['num_proyecto'] = num_proyecto
            reglas = Regla.objects.filter(proyecto=num_proyecto)
            context['reglas'] = reglas
            for re in reglas:
                if re.modo_pago == 2:
                    context['t_enganche_minimo'] = re.tipo_enganche_minimo
                    context['v_enganche_minimo'] = re.valor3
    #  Proyecto
            nom_proy = proyecto_tb[0].nom_proy
    # Agregar solicitud
            des_permiso = '_add_solicitud'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso
    # Cambiar solicitud
            des_permiso = '_cambia_solicitud'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso
    # Asigna descuento solicitud
            des_permiso = '_asigna_descto'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso

            asesor = self.request.POST.get('asesor')
            lote = self.request.POST.get('lote')

            context["asesor"] = asesor
            context["lote"] = lote
            context["cliente"] = cliente

            context["modo_pago"] = modo_pago
            context["tipo_descuento"] = tipo_descuento
            context["asigna_descuento"] = asigna_descuento
            context["cantidad_pagos"] = cantidad_pagos

            context["precio_lote"] = precio_lote
            context["precio_final"] = precio_final
            context["porcentaje_descuento"] = porcentaje_descuento
            context["descuento"] = descuento
            context["enganche"] = enganche
            context["importe_x_pago"] = importe_x_pago
            context["total"] = total
            context["precio_x_mt"] = precio_x_mt

            context["foto_elector_frente"] = foto_elector_frente
            context["foto_elector_reverso"] = foto_elector_reverso
            context["foto_comprobante"] = foto_comprobante
            context["foto_matrimonio"] = foto_matrimonio
            context["estatus_solicitud"] = estatus_solicitud
            context["foto_elector_frente_cy"] = foto_elector_frente_cy
            context["foto_elector_reverso_cy"] = foto_elector_reverso_cy
            context["foto_alta_shcp"] = foto_alta_shcp
            context["foto_acta_const"] = foto_acta_const
            context["tipo_cliente"] = tipo_cliente

            context["razon"] = razon
            context["nombre"] = nombre
            context["paterno"] = paterno
            context["materno"] = materno
            context["nombre_conyuge"] = nombre_conyuge
            context["paterno_conyuge"] = paterno_conyuge
            context["materno_conyuge"] = materno_conyuge
            context["rfc"] = rfc
            context["curp"] = curp
            context["estado_civil"] = estado_civil
            context["regimen"] = regimen
            context["calle"] = calle
            context["colonia"] = colonia
            context["codpos"] = codpos
            context["municipio"] = municipio
            context["estado"] = estado
            context["celular"] = celular
            context["correo"] = correo
            form = solicitud_valida
            context['form'] = form
            return render(self.request, self.template_name, context)
        
#        if form.is_valid():
#            solicitud1 = form.save()
#            guarda_cliente(self.request)
#            return HttpResponseRedirect(self.get_success_url())
#        else:
#            form = self.form_class(request.POST, request.FILES)
#            return render(request, self.template_name, {'form': form})

class mod_solicitud(UpdateView): 
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
                query1 = Q(tipo_empleado='E', area_operativa=3)
#                query2 = Q(id=f_empleado(self))
#                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
                empleado_cmb = Empleado.objects.filter(query1)  \
                    .filter(subidPersdonal__in=Subquery(gerente.values('pk'))) \
                    .order_by('paterno','materno','nombre').all()
            else:
                empleado_cmb = Empleado.objects.filter(id=f_empleado(self)) \
                    .order_by('paterno','materno','nombre')
            context['empleado_cmb'] = empleado_cmb
#        context['form'] = self.form_class()
        cliente_cmb = Cliente.objects.filter(estatus_cliente=1)
        context['cliente_cmb'] = cliente_cmb
        context['menu'] = "solicitud"
        context['accion'] = "Modifica"
        context['id'] = pk
        context['sol'] = Solicitud.objects.filter(id = pk)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
        reglas = Regla.objects.filter(proyecto=num_proyecto)
        context['reglas'] = reglas
        for re in reglas:
            if re.modo_pago == 2:
                context['t_enganche_minimo'] = re.tipo_enganche_minimo
                context['v_enganche_minimo'] = re.valor3

#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Agregar solicitud
        des_permiso = '_add_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Cambiar solicitud
        des_permiso = '_cambia_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Asigna descuento solicitud
        des_permiso = '_asigna_descto'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso

#       Datos Solicitud
        solicitud = Solicitud.objects.filter(id=pk)

        context["asesor"] = solicitud[0].asesor.id
        context["lote"] = solicitud[0].lote.id
        context["cliente"] = solicitud[0].cliente.id

        context["modo_pago"] = solicitud[0].modo_pago
        context["tipo_descuento"] = solicitud[0].tipo_descuento
        context["asigna_descuento"] = solicitud[0].asigna_descuento
        context["cantidad_pagos"] = solicitud[0].cantidad_pagos

        context["precio_lote"] = solicitud[0].precio_lote
        context["precio_final"] = solicitud[0].precio_final
        context["porcentaje_descuento"] = solicitud[0].porcentaje_descuento
        context["descuento"] = solicitud[0].descuento
        context["enganche"] = solicitud[0].enganche
        context["importe_x_pago"] = solicitud[0].importe_x_pago
        context["total"] = solicitud[0].total
        context["precio_x_mt"] = solicitud[0].precio_x_mt

        context["foto_elector_frente"] = solicitud[0].foto_elector_frente
        context["foto_elector_reverso"] = solicitud[0].foto_elector_reverso
        context["foto_comprobante"] = solicitud[0].foto_comprobante
        context["foto_matrimonio"] = solicitud[0].foto_matrimonio
        context["estatus_solicitud"] = solicitud[0].estatus_solicitud
        context["foto_elector_frente_cy"] = solicitud[0].foto_elector_frente_cy
        context["foto_elector_reverso_cy"] = solicitud[0].foto_elector_reverso_cy
        context["foto_alta_shcp"] = solicitud[0].foto_alta_shcp
        context["foto_acta_const"] = solicitud[0].foto_acta_const
        context["tipo_cliente"] = solicitud[0].tipo_cliente

        context["razon"] = solicitud[0].razon
        context["nombre"] = solicitud[0].nombre
        context["paterno"] = solicitud[0].paterno
        context["materno"] = solicitud[0].materno
        context["nombre_conyuge"] = solicitud[0].nombre_conyuge
        context["paterno_conyuge"] = solicitud[0].paterno_conyuge
        context["materno_conyuge"] = solicitud[0].materno_conyuge
        context["rfc"] = solicitud[0].rfc
        context["curp"] = solicitud[0].curp
        context["estado_civil"] = solicitud[0].estado_civil
        context["regimen"] = solicitud[0].regimen
        context["calle"] = solicitud[0].calle
        context["colonia"] = solicitud[0].colonia
        context["codpos"] = solicitud[0].codpos
        context["municipio"] = solicitud[0].municipio
        context["estado"] = solicitud[0].estado
        context["celular"] = solicitud[0].celular
        context["correo"] = solicitud[0].correo
        return context
#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object
#        id_solicitud = kwargs['pk']
#        solicitud = self.model.objects.get(id=id_solicitud)
#        form = self.form_class(request.POST, request.FILES, instance=solicitud)
#        if form.is_valid():
#            form.save()
#            guarda_cliente(self.request)
 #           return HttpResponseRedirect(self.get_success_url())
#        return self.render_to_response(self.get_context_data(form=form))
#    def get_success_url(self):
#        num_proyecto = self.kwargs.get('num_proyecto',0)
#        return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
        cliente = request.POST.get('cliente')
        asesor = request.POST.get('asesor')
        lote = request.POST.get('lote')

        modo_pago = int(request.POST.get('modo_pago').replace(',',''))
        tipo_descuento = int(request.POST.get('tipo_descuento').replace(',',''))
        asigna_descuento = request.POST.get('asigna_descuento')
        cantidad_pagos = request.POST.get('cantidad_pagos')

        precio_lote = request.POST.get('precio_lote').replace(',','')
        precio_final = request.POST.get('precio_final').replace(',','')
        porcentaje_descuento = request.POST.get('porcentaje_descuento').replace(',','')
        descuento = request.POST.get('descuento').replace(',','')
        enganche = request.POST.get('enganche').replace(',','')
        importe_x_pago = request.POST.get('importe_x_pago').replace(',','')
        total = request.POST.get('total').replace(',','')
        precio_x_mt = request.POST.get('precio_x_mt').replace(',','')

        foto_elector_frente = request.POST.get('foto_elector_frente')
        foto_elector_reverso = request.POST.get('foto_elector_reverso')
        foto_comprobante = request.POST.get('foto_comprobante')
        foto_matrimonio = request.POST.get('foto_matrimonio')
        estatus_solicitud = request.POST.get('estatus_solicitud')
        foto_elector_frente_cy = request.POST.get('foto_elector_frente_cy')
        foto_elector_reverso_cy = request.POST.get('foto_elector_reverso_cy')
        foto_alta_shcp = request.POST.get('foto_alta_shcp')
        foto_acta_const = request.POST.get('foto_acta_const')
        tipo_cliente = request.POST.get('tipo_cliente')

        razon = request.POST.get('razon')
        nombre = request.POST.get('nombre')
        paterno = request.POST.get('paterno')
        materno = request.POST.get('materno')
        nombre_conyuge = request.POST.get('nombre_conyuge')
        paterno_conyuge = request.POST.get('paterno_conyuge')
        materno_conyuge = request.POST.get('materno_conyuge')
        
        rfc = request.POST.get('rfc')
        curp = request.POST.get('curp')
        estado_civil = request.POST.get('estado_civil')
        regimen = request.POST.get('regimen')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        codpos = request.POST.get('codpos')
        municipio = request.POST.get('municipio')
        estado = request.POST.get('estado')
        celular = request.POST.get('celular')
        correo = request.POST.get('correo')

        data = {
            'cliente':cliente,
            'asesor':asesor,
            'lote':lote,
            'precio_lote':precio_lote,
            'precio_final':precio_final,
            'tipo_descuento':tipo_descuento,
            'asigna_descuento':asigna_descuento,
            'porcentaje_descuento':porcentaje_descuento,
            'descuento':descuento,
            'modo_pago':modo_pago,
            'enganche':enganche,
            'cantidad_pagos':cantidad_pagos,
            'importe_x_pago':importe_x_pago,
            'foto_elector_frente':foto_elector_frente,
            'foto_elector_reverso':foto_elector_reverso,
            'foto_comprobante':foto_comprobante,
            'foto_matrimonio':foto_matrimonio,
            'estatus_solicitud':estatus_solicitud,
            'foto_elector_frente_cy':foto_elector_frente_cy,
            'foto_elector_reverso_cy':foto_elector_reverso_cy,
            'foto_alta_shcp':foto_alta_shcp,
            'foto_acta_const':foto_acta_const,
            'tipo_cliente':tipo_cliente,
            'razon':razon,
            'nombre':nombre,
            'paterno':paterno,
            'materno':materno,
            'nombre_conyuge':nombre_conyuge,
            'paterno_conyuge':paterno_conyuge,
            'materno_conyuge':materno_conyuge,
            'rfc':rfc,
            'curp':curp,
            'estado_civil':estado_civil,
            'regimen':regimen,
            'calle':calle,
            'colonia':colonia,
            'codpos':codpos,
            'municipio':municipio,
            'estado':estado,
            'celular':celular,
            'correo':correo,
            'total':total,
            'precio_x_mt':precio_x_mt,
        }
        solicitud_valida = Nuvole_SolicitudForm(data)

        if solicitud_valida.is_valid():
            solicitud_upd = Solicitud.objects.get(id=pk)
            solicitud_upd.cliente.id = cliente
            solicitud_upd.asesor.id = asesor
            solicitud_upd.lote.id = lote
            solicitud_upd.precio_lote = precio_lote
            solicitud_upd.precio_final = precio_final
            solicitud_upd.tipo_descuento = tipo_descuento
            solicitud_upd.asigna_descuento = asigna_descuento
            solicitud_upd.porcentaje_descuento = porcentaje_descuento
            solicitud_upd.descuento = descuento
            solicitud_upd.modo_pago = modo_pago
            solicitud_upd.enganche = enganche
            solicitud_upd.cantidad_pagos = cantidad_pagos
            solicitud_upd.importe_x_pago = importe_x_pago
            solicitud_upd.foto_elector_frente = foto_elector_frente
            solicitud_upd.foto_elector_reverso = foto_elector_reverso
            solicitud_upd.foto_comprobante = foto_comprobante
            solicitud_upd.foto_matrimonio = foto_matrimonio
            solicitud_upd.estatus_solicitud = estatus_solicitud
            solicitud_upd.foto_elector_frente_cy = foto_elector_frente_cy
            solicitud_upd.foto_elector_reverso_cy = foto_elector_reverso_cy
            solicitud_upd.foto_alta_shcp = foto_alta_shcp
            solicitud_upd.foto_acta_const = foto_acta_const
            solicitud_upd.tipo_cliente = tipo_cliente
            solicitud_upd.razon = razon
            solicitud_upd.nombre = nombre
            solicitud_upd.paterno = paterno
            solicitud_upd.materno = materno
            solicitud_upd.nombre_conyuge = nombre_conyuge
            solicitud_upd.paterno_conyuge = paterno_conyuge
            solicitud_upd.materno_conyuge = materno_conyuge
            solicitud_upd.rfc = rfc
            solicitud_upd.curp = curp
            solicitud_upd.estado_civil = estado_civil
            solicitud_upd.regimen = regimen
            solicitud_upd.calle = calle
            solicitud_upd.colonia = colonia
            solicitud_upd.codpos = codpos
            solicitud_upd.municipio = municipio
            solicitud_upd.estado = estado
            solicitud_upd.celular = celular
            solicitud_upd.correo = correo
            solicitud_upd.total  = total
            solicitud_upd.precio_x_mt = precio_x_mt
            solicitud_upd.save()
            guarda_cliente(self.request)
#            return reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
            return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto},))
        else:
            context = {}
            context['num_proyecto'] = num_proyecto
            context['lote_cmb'] = Lote.objects.filter(proyecto=num_proyecto,estatus_lote=1).all()
            if 'empleado_cmb' not in context:
                asigna_solicitud = f_asigna_solicitud(self)
                f_emp = f_empleado(self)
                if asigna_solicitud:
                    query1 = Q(tipo_empleado='E', area_operativa=3) 
    #                query2 = Q(id=f_emp)
    #                empleado_cmb = Empleado.objects.filter(query1 | query2)  \
                    gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
                    empleado_cmb = Empleado.objects.filter(query1)  \
                        .filter(subidPersdonal__in=Subquery(gerente.values('pk'))) \
                        .order_by('paterno','materno','nombre').all()
                    context['f_emp'] = 0
                else:
                    empleado_cmb = Empleado.objects.filter(id=f_emp) \
                        .order_by('paterno','materno','nombre')
                    context['f_emp'] = f_emp
                context['empleado_cmb'] = empleado_cmb
    #        context['form'] = self.form_class(self.request.GET)
            cliente_cmb = Cliente.objects.filter(estatus_cliente=1)
            context['cliente_cmb'] = cliente_cmb
            context['menu'] = "solicitud"
            context['accion'] = "Alta"
            context['sol'] = Solicitud.objects.filter(id = 0)
            proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
            context['proyecto_tb'] = proyecto_tb
            context['num_proyecto'] = num_proyecto
            reglas = Regla.objects.filter(proyecto=num_proyecto)
            context['reglas'] = reglas
            for re in reglas:
                if re.modo_pago == 2:
                    context['t_enganche_minimo'] = re.tipo_enganche_minimo
                    context['v_enganche_minimo'] = re.valor3
    #  Proyecto
            nom_proy = proyecto_tb[0].nom_proy
    # Agregar solicitud
            des_permiso = '_add_solicitud'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso
    # Cambiar solicitud
            des_permiso = '_cambia_solicitud'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso
    # Asigna descuento solicitud
            des_permiso = '_asigna_descto'
            variable_proy = nom_proy + des_permiso
            variable_html = "app_proy" + des_permiso
            permiso_str = "gestion." + variable_proy
            acceso = self.request.user.has_perms([permiso_str])
            context[variable_html] = acceso
            asesor = self.request.POST.get('asesor')
            lote = self.request.POST.get('lote')

            context["asesor"] = asesor
            context["lote"] = lote
            context["cliente"] = cliente

            context["modo_pago"] = modo_pago
            context["tipo_descuento"] = tipo_descuento
            context["asigna_descuento"] = asigna_descuento
            context["cantidad_pagos"] = cantidad_pagos

            context["precio_lote"] = precio_lote
            context["precio_final"] = precio_final
            context["porcentaje_descuento"] = porcentaje_descuento
            context["descuento"] = descuento
            context["enganche"] = enganche
            context["importe_x_pago"] = importe_x_pago
            context["total"] = total
            context["precio_x_mt"] = precio_x_mt

            context["foto_elector_frente"] = foto_elector_frente
            context["foto_elector_reverso"] = foto_elector_reverso
            context["foto_comprobante"] = foto_comprobante
            context["foto_matrimonio"] = foto_matrimonio
            context["estatus_solicitud"] = estatus_solicitud
            context["foto_elector_frente_cy"] = foto_elector_frente_cy
            context["foto_elector_reverso_cy"] = foto_elector_reverso_cy
            context["foto_alta_shcp"] = foto_alta_shcp
            context["foto_acta_const"] = foto_acta_const
            context["tipo_cliente"] = tipo_cliente

            context["razon"] = razon
            context["nombre"] = nombre
            context["paterno"] = paterno
            context["materno"] = materno
            context["nombre_conyuge"] = nombre_conyuge
            context["paterno_conyuge"] = paterno_conyuge
            context["materno_conyuge"] = materno_conyuge
            context["rfc"] = rfc
            context["curp"] = curp
            context["estado_civil"] = estado_civil
            context["regimen"] = regimen
            context["calle"] = calle
            context["colonia"] = colonia
            context["codpos"] = codpos
            context["municipio"] = municipio
            context["estado"] = estado
            context["celular"] = celular
            context["correo"] = correo
            form = solicitud_valida
            context['form'] = form

            return render(self.request, self.template_name, context)

def can_sol(request, llave, num_proyecto):
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_cancela_solicitud'
    variable_proy = nom_proy + des_permiso
    variable_html = "app_proy" + des_permiso
    permiso_str = "gestion." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        sol = Solicitud.objects.filter(id=llave).update(estatus_solicitud='99', apartado=0)
        return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto},))

def rec_sol(request, llave, num_proyecto):
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_cancela_solicitud'
    variable_proy = nom_proy + des_permiso
    variable_html = "app_proy" + des_permiso
    permiso_str = "gestion." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        sol = Solicitud.objects.filter(id=llave).update(estatus_solicitud='1')
        return HttpResponseRedirect(reverse('solicitudes', kwargs={'num_proyecto':num_proyecto} ,))

class autorizaciones(ListView):
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
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersdonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
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
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado autorizaciones
        des_permiso = '_autoriza_visualiza'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Autorización ventas 
        des_permiso = '_autoriza_venta'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Autorización desarrollo
        des_permiso = '_autoriza_desarrollo'
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

def aut_ventas(request, llave, num_proyecto):
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_autoriza_venta'
    variable_proy = nom_proy + des_permiso
    variable_html = "app_proy" + des_permiso
    permiso_str = "gestion." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        sol = Solicitud.objects.filter(id=llave).update(aprobacion_gerente=True)
        return HttpResponseRedirect(reverse(('autorizaciones'), kwargs={'num_proyecto':num_proyecto} ,))

def aut_desarrollo(request, llave, num_proyecto):
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_autoriza_desarrollo'
    variable_proy = nom_proy + des_permiso
    variable_html = "app_proy" + des_permiso
    permiso_str = "gestion." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        sol = Solicitud.objects.filter(id=llave).update(aprobacion_director=True)
        return HttpResponseRedirect(reverse(('autorizaciones'), kwargs={'num_proyecto':num_proyecto} ,))

class compromisos(ListView):
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
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersdonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
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
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['num_proyecto'] = num_proyecto
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado compromisos
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Realizar compromiso 
        des_permiso = '_pago_compromiso'
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

class pagos(UpdateView): 
    model = Solicitud
    form_class = Nuvole_CompromisoForm
    template_name = 'gestion/pagos.html'
    def get_context_data(self, **kwargs):
        context = super(pagos, self).get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
        context['num_proyecto'] = num_proyecto
        context['pk'] = pk
        pk = self.kwargs.get('pk',0)
        context['sol'] = Solicitud.objects.filter(id=pk)
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Realizar listado pagos compromiso
        des_permiso = '_compromiso'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Realizar pago compromiso
        des_permiso = '_pago_compromiso'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Confirma depósito pago
        des_permiso = '_confirma_deposito_pago'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Impresion recibos pagos
        des_permiso = '_imp_pago_compromiso'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
    def get_queryset(self):
        pk = self.kwargs.get('pk',0)
        queryset = Solicitud.objects.all().filter(id=pk)
        return queryset
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
        solicitud = self.model.objects.get(id=pk)
        form = self.form_class(request.POST, request.FILES, instance=solicitud)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                numero_lote = request.POST.get('lote')
                num_contrato_sol = request.POST.get('num_contrato')
                estatus = request.POST.get('estatus_solicitud')
                confirmacion_pago_adicional = request.POST.get('confirmacion_pago_adicional')
                precio_final = request.POST.get('precio_final')
                solis = Solicitud.objects.filter(id=pk)
                lote = Lote.objects.filter(id=numero_lote).update(estatus_lote=estatus)
                solicitud_bus = Solicitud.objects.filter(estatus_solicitud=1,lote=numero_lote) \
                    .update(estatus_solicitud=5)
                solicitud_actual = Solicitud.objects.filter(id=pk).update(estatus_solicitud=estatus)
#   Asignar numero de contrato a la solicitud        
                autorizado = 0
                if not num_contrato_sol:
                    num_contrato_sol = '0'
                if confirmacion_pago_adicional == '2' and num_contrato_sol == '0':
                    num_contrato = Folios.objects.filter(tipo=2).aggregate(Max('numero'))['numero__max']
                    if num_contrato == None:
                        num_contrato = 1
                    else:
                        num_contrato += 1
                    dato = str(solis[0].lote) + \
                        " del proyecto: " + str(solis[0].lote.proyecto)
                    observacion = "Contrato del " + dato
                    folio = Folios(
                        tipo = 2, 
                        numero = num_contrato,
                        observacion = observacion,
                        importe = precio_final)
                    folio.save()
                    sol = Solicitud.objects.filter(id=pk) \
                        .update(num_contrato=num_contrato)
        return HttpResponseRedirect(self.get_success_url())
#        return self.render_to_response(self.get_context_data(form=form))
    def get_success_url(self):
        pk = self.kwargs.get('pk',0)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        return reverse_lazy('pagos', kwargs={'num_proyecto': num_proyecto, 'pk': pk})

class archivo(ListView):
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
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersdonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk')))
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
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado de archivo solicitudes
        des_permiso = '_consulta_archivo'
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

class reciboPDF(View):
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

class contratos(ListView):
    model = Solicitud
    second_model = Lote
    context_object_name = 'obj'
    template_name = 'gestion/contratos.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        asigna_solicitud = f_asigna_solicitud(self)
        proyecto = self.kwargs.get('num_proyecto',0)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=proyecto)
        if asigna_solicitud:
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersdonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(apartado__gt=0,confirmacion_apartado=1)
        else:
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(asesor_id=id_empleado) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk')))
        return queryset
    def get_context_data(self, **kwargs):
        context = super(contratos, self).get_context_data(**kwargs)
        context['menu'] = "contrata"
        num_proyecto = self.kwargs.get('num_proyecto',0)
        context['num_proyecto'] = num_proyecto
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
        des_permiso = '_contratar'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Capturar datos contrato   
        des_permiso = '_datos_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Impresión contrato
        des_permiso = '_imprime_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
# Archivar contrato 
        des_permiso = '_archivar_contrato'
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
        context['reporte'] = "/gestion/contratoPDF/"
        context['reporte1'] = "/finanzas/lista_pagos_PDF/"
        return context

class datos_contrato(UpdateView): 
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
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
        des_permiso = '_datos_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
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
        #  Asesor
        field_object = Solicitud._meta.get_field('asesor')
        asesor = field_object.value_from_object(solicitud)
        #  Lote
        field_object = Solicitud._meta.get_field('lote')
        lote = field_object.value_from_object(solicitud)
        #  Fecha Confirma Pago Adicional
        field_object = Solicitud._meta.get_field('fecha_confirma_pago_adicional')
        fecha_confirma_pago_adicional = field_object.value_from_object(solicitud)
        #  Fecha Contrato
        fecha_contrato = request.POST.get('fecha_contrato')
        diferencia = precio_final - enganche
        form = self.form_class(request.POST, instance=solicitud)
        if form.is_valid():
            with transaction.atomic():
                form.save()
#   Genera registo de pago de comisión
                lote_actual = Lote.objects.filter(id=lote)
                id_proyecto = lote_actual[0].proyecto.id
                comision = comision_asesor(asesor, id_proyecto, False)
                jefe = Empleado.objects.filter(id=asesor)
                gerente = jefe[0].subidPersdonal
                comision_gerente = comision_asesor(gerente, id_proyecto, True)
                comision_publicidad = COMISION_PUBLICIDAD
                importe = precio_final * comision / 100
                importe_gerente = precio_final * comision_gerente / 100
                importe_publicidad = precio_final * comision_publicidad / 100
                pagoComision = PagoComision(proyecto_pago_id=id_proyecto, empleado_pago_id=asesor, bien_pago_id=lote, modo_pago=modo_pago, \
                    precio_final=precio_final, enganche=enganche, fecha_confirma_pago_adicional=fecha_confirma_pago_adicional, \
                    fecha_contrato=fecha_contrato, comsion=comision, importe=importe, comsion_gerente=comision_gerente, \
                    importe_gerente=importe_gerente, comsion_publicidad=comision_publicidad, importe_publicidad=importe_publicidad)
                pagoComision.save()
                if modo_pago == 1:
                    sol = Solicitud.objects.filter(id=self.kwargs['pk']) \
                        .update(estatus_solicitud=9)
                    a=0
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
    proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
    nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
    des_permiso = '_archivar_contrato'
    variable_proy = nom_proy + des_permiso
    permiso_str = "gestion." + variable_proy
    acceso = request.user.has_perms([permiso_str])
    if acceso:
        if estado == "6":
            archiva_solicitud = Solicitud.objects.filter(id=id).update(estatus_solicitud = 7)
        else:
            if estado == "99":
                archiva_solicitud = Solicitud.objects.filter(id=id).update(estatus_solicitud = 8)
        
    return reverse('contratos', kwargs={'num_proyecto': num_proyecto})

class contratoPDF(CreateView):
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

#        result = finders.find(uri)
#        if result:
#                if not isinstance(result, (list, tuple)):
#                        result = [result]
#                result = list(os.path.realpath(path) for path in result)
#                path=result[0]
#        else:

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
        num_proyecto = self.kwargs['num_proyecto']
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
#  Proyecto
        nom_proy = proyecto_tb[0].nom_proy
# Listado contratos
        des_permiso = '_datos_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        if acceso:
            solicitud = Solicitud.objects.all().filter(id=self.kwargs['pk']).first()
            template_contrato = 'gestion/' + nom_proy + '_contratoPDF.html'
#            template = get_template('gestion/contratoPDF.html')
            template = get_template(template_contrato)
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
            importe_x_pago_l = numero_a_letras(importe_x_pago_i)

            saldo = precio_final - enganche
            saldo_i = int(saldo)
            saldo_d = str(abs(saldo) - abs(int(saldo)))[-2:]
            saldo_l = numero_a_letras(saldo_i)

            importe_total_x_pagos = importe_x_pago * cantidad_pagos

            ultimo_pago = importe_x_pago - (importe_total_x_pagos - saldo)
            ultimo_pago_i = int(ultimo_pago)
            ultimo_pago_d = str(abs(ultimo_pago) - abs(int(ultimo_pago)))[-2:]
            ultimo_pago_l = numero_a_letras(ultimo_pago_i)

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

#            if num_contrato != 0:
            num_contrato = num_contrato
#            else: 
#  Asiganr numero de contrato a la solcititud                
#                num_contrato = Folios.objects.filter(tipo=2).aggregate(Max('numero'))['numero__max']
#                if num_contrato == None:
#                    num_contrato = 1
#                else:
#                    num_contrato += 1
#                if modo_pago == 1 or modo_pago == 3:
#                    esta_sol = 6
#                else:
#                    esta_sol = 10
#                dato = str(solicitud.lote) + \
#                    " del proyecto: " + str(solicitud.lote.proyecto)
#                observacion = "Contrato del " + dato
#                folio = Folios(
#                    tipo = 2, 
#                    numero = num_contrato,
#                    observacion = observacion,
#                    importe = precio_final)
#                folio.save()
#                sol = Solicitud.objects.filter(id=self.kwargs['pk'])   \
#                    .update(num_contrato=num_contrato, estatus_solicitud=esta_sol)
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
                'importe_x_pago_l':importe_x_pago_l,
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
                'ultimo_pago_l':ultimo_pago_l,
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
#    def get_queryset(self):
#        queryset = Solicitud.objects.all()
#        return queryset

def vobo_comisiones(request, fecha_hasta_str, num_proyecto, fecha_hasta, nom_proyecto, imp_ger, imp_pub):
    fecha_hasta1 = str_to_fecha_amd(fecha_hasta)
    fecha_desde_p = fecha_inicio_dia_mes_pago(fecha_hasta1)
    fecha_hasta_p = fecha_ultimo_dia_mes_pago(fecha_hasta1)
#    with transaction.atomic():
    folio_gerente = nuevo_folio(3)
    observacion = "Comisión gerente de fecha " + fecha_hasta_str + \
        " del proyecto " + nom_proyecto
    folio = Folios(
        tipo = 3, 
        numero = folio_gerente,
        observacion = observacion,
        importe = imp_ger)
    folio.save()
    folio_publicidad = nuevo_folio(3)
    observacion = "Comisión publicidad de fecha " + fecha_hasta_str + \
        " del proyecto " + nom_proyecto
    folio = Folios(
        tipo = 3, 
        numero = folio_publicidad,
        observacion = observacion,
        importe = imp_pub)
    folio.save()
    empleado_ant = 0
    pago_comision_detalle = PagoComision.objects \
        .filter(fecha_contrato__range=[fecha_desde_p, fecha_hasta_p], proyecto_pago=num_proyecto) 
    for pago in pago_comision_detalle:
        if not pago.empleado_pago == empleado_ant:
            empleado_ant = pago.empleado_pago
            folio_asesor = nuevo_folio(3)
            observacion = "Comisión agente " + pago.empleado_pago.nombre_completo + \
                " de fecha " + fecha_hasta_str + " del proyecto " + nom_proyecto
            folio = Folios(
                tipo = 3, 
                numero = folio_asesor,
                observacion = observacion,
                importe = pago.importe)
            folio.save()
        actualiza = PagoComision.objects \
            .filter(bien_pago=pago.bien_pago) \
            .update(estatus_comision=1,fecha_periodo=fecha_hasta,folio_comision_gerente=folio_gerente, \
                folio_comision_publicidad=folio_publicidad,folio_comision_asesor=folio_asesor)
    return HttpResponseRedirect(reverse_lazy(('pago_comisiones'), kwargs={'num_proyecto':num_proyecto,'id_periodo':fecha_hasta_str} ,))
