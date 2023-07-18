from django.contrib.sessions.backends.db import SessionStore
from multiprocessing import context 
import os
import datetime
from django.db.models import Max, Q, Subquery
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
import decimal
from django.http import JsonResponse
import math
import json

from core.models import *
from .funciones import *
from .forms import *
from core.numero_letras import numero_a_letras
from core.funciones import *
from bien.models import Lote

@login_required
def calcula_operacion(request, descuento, porcentaje_descuento, modo_pago, idLote, enganche, cantidad_pagos, asigna_descuento, tipo_desc):
    lote = Lote.objects.filter(id=idLote)
    num_proyecto = lote[0].proyecto.id
    precio = lote[0].precio
    total = lote[0].total
    precio_x_mt = lote[0].precio_x_mt
    if '-' in cantidad_pagos:
        cantidad_pagos, id = cantidad_pagos.split('-')
        regla = Regla.objects.filter(id=id)
    else:
        regla = Regla.objects.filter(proyecto_id=num_proyecto, modo_pago=modo_pago , mensualidades_permitidas=cantidad_pagos)

    precio_final = precio

    if asigna_descuento == '1':
        if regla:
            tipo_aplica_descto = regla[0].tipo_aplica_descto
            if tipo_aplica_descto != 0:
                valor1 = regla[0].valor1
                if tipo_aplica_descto == 1:                        #  Importe por metro cuadrado
                    precio_x_mt = precio_x_mt + valor1
                    precio = total * precio_x_mt
                    precio_final = precio
                elif tipo_aplica_descto == 2:                      #  % por metro cuadrado
                    descuento_mt = ((precio_x_mt * valor1) / 100)
                    precio_x_mt = precio_x_mt + descuento_mt
                    precio = total * precio_x_mt
                    precio_final = precio
        if tipo_desc == '1':
            descuento = (precio * decimal.Decimal(porcentaje_descuento)) / 100
            precio_final = precio - decimal.Decimal(descuento)
        elif tipo_desc == '2':
            precio_final = precio - decimal.Decimal(descuento)
    else:
        descuento = 0
        porcentaje_descuento = 0
        if regla:
            tipo_aplica_descto = regla[0].tipo_aplica_descto
            if tipo_aplica_descto != 0:
                valor1 = regla[0].valor1
                if tipo_aplica_descto == 1:                        #  Importe por metro cuadrado
                    precio_x_mt = precio_x_mt + valor1
                    precio = total * precio_x_mt
                    precio_final = precio
                elif tipo_aplica_descto == 2:                      #  % por metro cuadrado
                    descuento_mt = ((precio_x_mt * valor1) / 100)
                    precio_x_mt = precio_x_mt + descuento_mt
                    precio = total * precio_x_mt
                    precio_final = precio
                elif tipo_aplica_descto == 3:                      # Importe al precio de lista
                    descuento = valor1
                    porcentaje_descuento = 0
                    precio_final = precio + descuento
                elif tipo_aplica_descto == 4:                      # % al precio de lista
                    porcentaje_descuento = valor1
                    descuento = ((precio * decimal.Decimal(porcentaje_descuento)) / 100)
                    precio_final = precio + descuento
    error_enganche = ''
    enganche_calculado = 0
    importe_formateado = 0
    if regla:
        tipo_enganche_minimo = regla[0].tipo_enganche_minimo
        valor3 = regla[0].valor3
        if tipo_enganche_minimo == 1:
            enganche_calculado = valor3
        else:
            enganche_calculado = (decimal.Decimal(precio_final) * decimal.Decimal(valor3)) / decimal.Decimal('100')
        if decimal.Decimal(enganche) < enganche_calculado:
            importe_formateado = "{:,.2f}".format(enganche_calculado)
            error_enganche = '<label class="text-danger" >' + "El enganche mínimo es " + str(importe_formateado) + '</label>'
    
    pago_mensual = 0
    credito = 0
    if modo_pago != '1':
        credito = precio_final - decimal.Decimal(enganche)
        if decimal.Decimal(cantidad_pagos) > 0:
            pago_mensual = math.ceil(float((precio_final - decimal.Decimal(enganche)) / decimal.Decimal(cantidad_pagos)) * 100) / 100
    datos= {}
    datos['total'] = "{:,.2f}".format(total)
    datos['precio_x_mt'] = "{:,.2f}".format(precio_x_mt)
    datos['precio'] = "{:,.2f}".format(precio)
    datos['descuento'] = "{:,.2f}".format(decimal.Decimal(descuento))
    datos['precio_final'] = "{:,.2f}".format(precio_final)
    datos['credito'] = "{:,.2f}".format(credito)
    datos['porcentaje_descuento'] = "{:,.2f}".format(decimal.Decimal(porcentaje_descuento))
    datos['enganche'] = "{:,.2f}".format(decimal.Decimal(enganche))
    datos['pago_mensual'] = "{:,.2f}".format(pago_mensual)
    datos['error_enganche'] = error_enganche
    datos['asigna_descuento'] = asigna_descuento
    datos['tipo_desc'] = tipo_desc
    datos['enganche_calculado'] = enganche_calculado
    datos['importe_formateado'] = importe_formateado
    return JsonResponse({'datos': datos})

@login_required
def valida_enganche_minimo(request, proyecto, modo_pago, precio, enganche, mensualidades):
    reglas = Regla.objects.filter(proyecto_id=proyecto, modo_pago=modo_pago , mensualidades_permitidas=mensualidades)
    valor3 = reglas[0].valor3
    if reglas[0].tipo_enganche_minimo == 1:
        importe = valor3
    else:
        importe = (decimal.Decimal(precio) * decimal.Decimal(valor3)) / decimal.Decimal('100')
    importe_formateado = "{:,.2f}".format(importe)
    if decimal.Decimal(enganche) < importe:
        respuesta = '<label class="text-danger" >' + "El enganche mínimo es " + str(importe_formateado) + '</label>'
    else:
        respuesta = ''
    return JsonResponse({'mensaje': respuesta})
    
@login_required
def valores_bien(request, id, importe):
    importe_dec = float(importe)
    datos = {}
    if id != '0':
        lote = Lote.objects.filter(id=id)
        importe_suma = lote[0].precio_x_mt + decimal.Decimal(importe_dec)
        importe_formateado = "{:,.2f}".format(importe_suma)
        datos['precio_x_mt'] = importe_formateado
        importe_operacion = lote[0].total * importe_suma
        importe_formateado = "{:,.2f}".format(importe_operacion)
        datos['precio'] = importe_formateado
    else:
        datos['precio_x_mt'] = 0
        datos['precio'] = 0
    return JsonResponse({'datos': datos})

@login_required
def valores_bien_inicial(request, id):
    datos = {}
    if id != '0':
        lote = Lote.objects.filter(id=id)
        importe_formateado = "{:,.2f}".format(lote[0].precio_x_mt)
        datos['precio_x_mt'] = importe_formateado
        importe_formateado = "{:,.2f}".format(lote[0].precio)
        datos['precio'] = importe_formateado
    else:
        datos['precio_x_mt'] = 0
        datos['precio'] = 0
    return JsonResponse({'datos': datos})

class solicitudes(ListView):
    model = Solicitud
    context_object_name = 'obj'
    template_name = 'gestion/solicitudes.html'
    paginate_by = settings.RENGLONES_X_PAGINA
    def get_queryset(self):
        num_proyecto = self.kwargs.get('num_proyecto')
        asigna_solicitud = f_asigna_solicitud(self)
        lotes = Lote.objects.all().only("proyecto","id").filter(proyecto=num_proyecto)
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,5,99]) \
                .filter(aprobacion_gerente=False, aprobacion_director=False)
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)
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
# ver mapa
        des_permiso = '_acceso'
        variable_proy = nom_proy + des_permiso
        variable_html = "menu_proy" + des_permiso
        permiso_str = "bien." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
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
        des_permiso = '_amortizac'
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

@login_required
def guarda_solicitud(request, id):
    if id == 0:
        gda_sol = Solicitud()
        gda_sol.estatus_solicitud = 1
    else:
        gda_sol = Solicitud.objects.get(id=id)
    gda_sol.cliente_id = request.POST.get('cliente')
    gda_sol.lote_id = request.POST.get('lote')
    gda_sol.asesor_id = request.POST.get('num_asesor')
    gda_sol.precio_lote = request.POST.get('precio_lote').replace(',', '').replace(',', '')
    gda_sol.total = request.POST.get('total').replace(',', '').replace(',', '')
    gda_sol.precio_x_mt = request.POST.get('precio_x_mt').replace(',', '').replace(',', '')
    gda_sol.precio_final = request.POST.get('precio_final').replace(',', '').replace(',', '')
    gda_sol.tipo_descuento = request.POST.get('tipo_descuento')
    gda_sol.porcentaje_descuento = request.POST.get('porcentaje_descuento')
    gda_sol.descuento = request.POST.get('descuento').replace(',', '').replace(',', '')
    gda_sol.modo_pago = request.POST.get('modo_pago')
    gda_sol.credito = request.POST.get('credito').replace(',', '').replace(',', '')
    gda_sol.enganche = request.POST.get('enganche').replace(',', '').replace(',', '')
    gda_sol.cantidad_pagos = request.POST.get('cantidad_pagos')
    gda_sol.importe_x_pago = request.POST.get('importe_x_pago').replace(',', '').replace(',', '')
    gda_sol.foto_elector_frente = request.POST.get('foto_elector_frente')
    gda_sol.foto_elector_reverso = request.POST.get('foto_elector_reverso')
    gda_sol.foto_elector_frente_cy = request.POST.get('foto_elector_frente_cy')
    gda_sol.foto_elector_reverso_cy = request.POST.get('foto_elector_reverso_cy')
    gda_sol.foto_matrimonio = request.POST.get('foto_matrimonio')
    gda_sol.foto_comprobante = request.POST.get('foto_comprobante')
    gda_sol.foto_alta_shcp = request.POST.get('foto_alta_shcp')
    gda_sol.foto_acta_const = request.POST.get('foto_acta_const')
    gda_sol.asigna_descuento = request.POST.get('asigna_descuento')
    gda_sol.porcentaje_descuento = request.POST.get('porcentaje_descuento')
    gda_sol.tipo_cliente = request.POST.get('tipo_cliente')
    gda_sol.razon = request.POST.get('razon')
    gda_sol.nombre = request.POST.get('nombre')
    gda_sol.paterno = request.POST.get('paterno')
    gda_sol.materno = request.POST.get('materno')
    gda_sol.nombre_conyuge = request.POST.get('nombre_conyuge')
    gda_sol.paterno_conyuge = request.POST.get('paterno_conyuge')
    gda_sol.materno_conyuge = request.POST.get('materno_conyuge')
    gda_sol.rfc = request.POST.get('rfc')
    gda_sol.curp = request.POST.get('curp')
    gda_sol.estado_civil = request.POST.get('estado_civil')
    gda_sol.regimen = request.POST.get('regimen')
    gda_sol.calle = request.POST.get('calle')
    gda_sol.colonia = request.POST.get('colonia')
    gda_sol.codpos = request.POST.get('codpos')
    gda_sol.municipio = request.POST.get('municipio')
    gda_sol.estado = request.POST.get('estado')
    gda_sol.celular = request.POST.get('celular')
    gda_sol.correo = request.POST.get('correo')
    gda_sol.save()
    nueva_solicitud = gda_sol.id
    guarda_cliente(request)
    return nueva_solicitud

@login_required
def selecciona_cliente(request, id):
    datos = {}
    cliente = get_object_or_404(Cliente, id=id)
    datos['tipo_cliente'] = cliente.tipo_cliente
    datos['razon'] = cliente.razon
    datos['nombre'] = cliente.nombre
    datos['paterno'] = cliente.paterno
    datos['materno'] = cliente.materno
    datos['nombre_conyuge'] = cliente.nombre_conyuge
    datos['paterno_conyuge'] = cliente.paterno_conyuge
    datos['materno_conyuge'] = cliente.materno_conyuge
    datos['rfc'] = cliente.rfc
    datos['curp'] = cliente.curp
    datos['estado_civil'] = cliente.estado_civil
    datos['regimen'] = cliente.regimen
    datos['calle'] = cliente.calle
    datos['colonia'] = cliente.colonia
    datos['codpos'] = cliente.codpos
    datos['municipio'] = cliente.municipio
    datos['estado'] = cliente.estado
    datos['celular'] = cliente.celular
    datos['correo'] = cliente.correo
    datos['nom_asesor'] = cliente.nombre_asesor
    datos['num_asesor'] = cliente.asesor.id
    return JsonResponse({'datos': datos})

@login_required
def selecciona_bien(request, id):
    datos = {}
    lote = get_object_or_404(Lote, id=id)
    precio = lote.precio
    precio_x_mt = lote.precio_x_mt
    total = lote.total
    datos['precio'] = precio
    datos['precio_x_mt'] = precio_x_mt
    datos['total'] = total
    return JsonResponse({'datos': datos})

def filtra_clientes(self):
    asigna_solicitud = f_asigna_solicitud(self)
    f_emp = f_empleado(self)
    datos = f_area_puesto(self)
    if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
        #  GERENTE
        gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
        empleados_gerente = Empleado.objects.filter(tipo_empleado='E', area_operativa=3, estatus_empleado=1)  \
            .filter(subidPersonal__in=Subquery(gerente.values('pk')))
        cliente_cmb = Cliente.objects.filter(asesor__in=Subquery(empleados_gerente.values('pk'))) \
            .filter(estatus_cliente=1)
    elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
        # DIRECTOR
        cliente_cmb = Cliente.objects.filter(estatus_cliente=1) \
            .order_by('paterno','materno','nombre').all()
    elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
        # DIRECTOR GENERAL
        cliente_cmb = Cliente.objects.filter(estatus_cliente=1) \
            .order_by('paterno','materno','nombre').all()
    elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
        # ASESOR
        cliente_cmb = Cliente.objects.filter(asesor=f_emp, estatus_cliente=1) \
            .order_by('paterno','materno','nombre')
    else:
        # SIN ACCESO
        cliente_cmb = Empleado.objects.filter(id=0)
    return cliente_cmb

class sol_nueva(CreateView):
    model = Solicitud
    form_class = Nuvole_SolicitudForm
    context_object_name = 'obj'
    template_name = 'gestion/sol_nueva.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = get_object_or_404(Proyecto, id=num_proyecto)
        context['list_url'] = reverse_lazy('sol_nueva', kwargs={'num_proyecto': num_proyecto})
        context['nombre_proyecto'] = proyecto_tb.nombre
        context['singular_proyecto'] = proyecto_tb.singular
        context['num_proyecto'] = num_proyecto
        context['lote_cmb'] = Lote.objects.filter(proyecto_id=num_proyecto,estatus_lote=1).all()
        context['cliente_cmb'] = filtra_clientes(self)
        context['empleado_cmb'] = Empleado.objects.filter(estatus_empleado=1)
        context['menu'] = "solicitud"
        context['accion'] = "Alta"
        context['reglas'] = Regla.objects.filter(proyecto=num_proyecto)
#  Proyecto
        nom_proy = proyecto_tb.nom_proy
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
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)   
        data = {}
        try:
            if form.is_valid():
                form.save()
            else:
                if hasattr(form, 'errors'):
                    if isinstance(form.errors, str):
                        # El atributo error tiene un valor
                        data['error'] = form.errors
                    elif isinstance(form.errors, dict):
                        # El atributo error tiene claves
                        bandera = False
                        for key, value in form.errors.items():
                            if 'Introduzca un número válido.' in value or 'Introduzca un número.' in value or 'el valor debe ser un número decimal.' in value:
                                pass
                            else:
                                bandera = True
                        if bandera:
                            data['error'] = form.errors
                        else:
                            nueva_solicitud = guarda_solicitud(request, 0)
                            data['nueva_solicitud'] = nueva_solicitud
                else:
                    # El atributo error no existe en el objeto
                    guarda_solicitud(request, 0)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class sol_editada(UpdateView):
    model = Solicitud
    form_class = Nuvole_SolicitudForm
    context_object_name = 'obj'
    template_name = 'gestion/sol_nueva.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = get_object_or_404(Proyecto, id=num_proyecto)
        context['list_url'] = reverse_lazy('solicitudes', kwargs={'num_proyecto': num_proyecto})
        context['nombre_proyecto'] = proyecto_tb.nombre
        context['singular_proyecto'] = proyecto_tb.singular
        context['num_proyecto'] = num_proyecto
        context['lote_cmb'] = Lote.objects.filter(proyecto=num_proyecto,estatus_lote=1).all()
        context['cliente_cmb'] = filtra_clientes(self)
        context['empleado_cmb'] = Empleado.objects.filter(estatus_empleado=1)
        context['menu'] = "solicitud"
        context['accion'] = "Modifica"
        context['pk'] = pk
        context['sol'] = Solicitud.objects.filter(id=pk)
        context['reglas'] = Regla.objects.filter(proyecto=num_proyecto)
#  Proyecto
        nom_proy = proyecto_tb.nom_proy
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
        return context
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)   
        pk = self.kwargs.get('pk',0)
        data = {}
        try:
            if form.is_valid():
                form.save()
            else:
                if hasattr(form, 'errors'):
                    if isinstance(form.errors, str):
                        # El atributo error tiene un valor
                        data['error'] = form.errors
                    elif isinstance(form.errors, dict):
                        # El atributo error tiene claves
                        bandera = False
                        for key, value in form.errors.items():
                            if 'Introduzca un número válido.' in value or 'Introduzca un número.' in value:
                                pass
                            else:
                                bandera = True
                        if bandera:
                            data['error'] = form.errors
                        else:
                            nueva_solicitud = guarda_solicitud(request, pk)
                            data['nueva_solicitud'] = nueva_solicitud
                else:
                    # El atributo error no existe en el objeto
                    guarda_solicitud(request, pk)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

@login_required
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

@login_required
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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .exclude(estatus_solicitud__in=[5,99]) \
                .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(estatus_solicitud__in=[5,99]) \
                .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(estatus_solicitud__in=[5,99]) \
                .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
            .filter(asesor_id=id_empleado) \
            .exclude(estatus_solicitud__in=[5,99]) \
            .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)

#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.all().filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .exclude(estatus_solicitud__in=[5,99]) \
#                .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#            .filter(asesor_id=id_empleado) \
#            .exclude(estatus_solicitud__in=[5,99]) \
#            .filter(Q(aprobacion_director=False) | Q(aprobacion_gerente=False))
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

@login_required
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

@login_required
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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        elif datos['area_operativa'] == 2:
            # Finanzas
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[2,3]) 
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(asesor_id=id_empleado) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(estatus_solicitud__in=[1,2,3]) 
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)


#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .filter(estatus_solicitud__in=[1,2,3]) 
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(asesor_id=id_empleado) \
#                .filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(estatus_solicitud__in=[1,2,3]) 
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
        sol = Solicitud.objects.filter(id=pk)
        context['sol'] = sol
        proyecto_tb = Proyecto.objects.filter(id=num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        context['apartado'] = sol[0].apartado
        context['pago_adicional'] = sol[0].pago_adicional
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
        valida = True
        if form.errors:
            for field in form:
                for error in field.errors:
                    if error != "Introduzca un número.":
                        if error != "Asegúrese de que no haya más de 2 dígitos decimales.":
                            valida = False
        if valida:
            with transaction.atomic():
                solicitud_upd = Solicitud.objects.get(id=pk)
                solicitud_upd.apartado = request.POST.get('apartado').replace(",","").replace(",","")
                solicitud_upd.confirmacion_apartado = request.POST.get('confirmacion_apartado')
                solicitud_upd.foto_comprobante_apartado = request.POST.get('foto_comprobante_apartado')
                solicitud_upd.forma_pago_apa = request.POST.get('forma_pago_apa')
                solicitud_upd.cuenta_apa = request.POST.get('cuenta_apa')
                solicitud_upd.numero_comprobante_apa = request.POST.get('numero_comprobante_apa')
                solicitud_upd.pago_adicional = request.POST.get('pago_adicional').replace(",","").replace(",","")
                solicitud_upd.confirmacion_pago_adicional = request.POST.get('confirmacion_pago_adicional')
                solicitud_upd.foto_comprobante_pago_adicional = request.POST.get('foto_comprobante_pago_adicional')
                solicitud_upd.forma_pago_pa = request.POST.get('forma_pago_pa')
                solicitud_upd.cuenta_pa = request.POST.get('cuenta_pa')
                solicitud_upd.numero_comprobante_pa = request.POST.get('numero_comprobante_pa')
                solicitud_upd.fecha_confirma_pago_adicional = request.POST.get('fecha_confirma_pago_adicional')
                solicitud_upd.estatus_solicitud = request.POST.get('estatus_solicitud')
                resultado = solicitud_upd.save()
#                form.save()
                numero_lote = request.POST.get('lote')
                num_contrato_sol = request.POST.get('num_contrato')
                estatus = request.POST.get('estatus_solicitud')
                confirmacion_pago_adicional = request.POST.get('confirmacion_pago_adicional')
                precio_final = request.POST.get('precio_final').replace(",","").replace(",","")
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
                    resultado = folio.save()
                    sol = Solicitud.objects.filter(id=pk) \
                        .update(num_contrato=num_contrato)
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = {}
            context["form"] = form
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

            apartado = request.POST.get('apartado')
            context["apartado"] = apartado
            pago_adicional = request.POST.get('pago_adicional')
            context["pago_adicional"] = pago_adicional

            return render(self.request, self.template_name, context)
#            return self.render_to_response(self.get_context_data(context=context))
    def get_success_url(self):
        num_proyecto = self.kwargs.get('num_proyecto',0)
        pk = self.kwargs.get('pk',0)
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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor__in=Subquery(empleados.values('pk')))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5:
            # DIRECTOR
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk')))
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk')))
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
                .filter(asesor_id=id_empleado)
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)
        
#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor__in=Subquery(empleados.values('pk')))
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(lote__in=Subquery(lotes.values('pk'))) \
#                .filter(asesor_id=id_empleado)
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
#  Consulta solicitud
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Archivar comprobantes
        des_permiso = '_archivar_comprobantes'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "finanzas." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
#  Impresión de contrato
        des_permiso = '_imprime_contrato'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        context['num_proyecto'] = num_proyecto
        context['reporte'] = "/gestion/contratoPDF/"
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
            if not num_recibo:
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
        centavos = "{:.2f}".format(round(importe, 2))[-2:]
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
                'centavos':centavos,
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
        datos = f_area_puesto(self)
        if asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 2:
            # GERENTE
            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(asesor__in=Subquery(empleados.values('pk'))) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(apartado__gt=0,confirmacion_apartado=1)
        elif (asigna_solicitud == 1 and datos['area_operativa'] == 3 and datos['puesto'] == 5) or  \
            (datos['area_operativa'] == 2 and datos['puesto'] == 4):
            # DIRECTOR Y PERSONAL DE FINANZAS
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(apartado__gt=0,confirmacion_apartado=1)
        elif asigna_solicitud == 1 and datos['area_operativa'] == 1 and datos['puesto'] == 3:
            # DIRECTOR GENERAL
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk'))) \
                .exclude(apartado__gt=0,confirmacion_apartado=1)
        elif datos['area_operativa'] == 3 and datos['puesto'] == 1:
            # ASESOR
            id_empleado = f_empleado(self)
            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
                .filter(asesor_id=id_empleado) \
                .filter(aprobacion_gerente=True, aprobacion_director=True) \
                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
                .filter(lote__in=Subquery(lotes.values('pk')))
        else:
            # SIN ACCESO
            queryset = Solicitud.objects.filter(asesor_id=0)

#        if asigna_solicitud == 1:
#            gerente = Empleado.objects.all().only("id").filter(usuario=self.request.user.id)
#            empleados = Empleado.objects.all().only("id").filter(subidPersonal__in=Subquery(gerente.values('pk')))
#            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
#                .filter(asesor__in=Subquery(empleados.values('pk'))) \
#                .filter(aprobacion_gerente=True, aprobacion_director=True) \
#                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
#                .filter(lote__in=Subquery(lotes.values('pk'))) \
#                .exclude(apartado__gt=0,confirmacion_apartado=1)
#        else:
#            id_empleado = f_empleado(self)
#            queryset = Solicitud.objects.filter(confirmacion_pago_adicional=2) \
#                .filter(asesor_id=id_empleado) \
#                .filter(aprobacion_gerente=True, aprobacion_director=True) \
#                .filter(estatus_solicitud__in=[3,4,6,9,10]) \
#                .filter(lote__in=Subquery(lotes.values('pk')))
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
                comision = obtener_comision(asesor, id_proyecto, False)
                jefe = Empleado.objects.filter(id=asesor)
                gerente = jefe[0].subidPersonal
                comision_gerente = obtener_comision(gerente, id_proyecto, True)
                comision_publicidad = COMISION_PUBLICIDAD
                importe = round(precio_final * comision / 100, 0)
                importe_gerente = round(precio_final * comision_gerente / 100, 0)
                importe_publicidad = round(precio_final * comision_publicidad / 100, 0)
                pagoComision = PagoComision(proyecto_pago_id=id_proyecto, asesor_pago_id=asesor, bien_pago_id=lote, modo_pago=modo_pago, \
                    precio_final=precio_final, enganche=enganche, fecha_confirma_pago_adicional=fecha_confirma_pago_adicional, \
                    fecha_contrato=fecha_contrato, comsion=comision, importe=importe, comsion_gerente=comision_gerente, \
                    importe_gerente=importe_gerente, comsion_publicidad=comision_publicidad, importe_publicidad=importe_publicidad, \
                    gerente_pago=gerente)
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
                                    fecha_pago=fecha_pago, importe_original=importe_x_pago)
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

@login_required
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
            
            #  Agregar los contratos a visualizar 
            
            if num_proyecto == '1' or num_proyecto == '2':
                template_contrato = 'gestion/' + nom_proy + '_contratoPDF.html'
            else:
                template_contrato = 'gestion/sin_contratoPDF.html'
                
                
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
            num_contrato_str = str(num_contrato)
#            else: 
#  Asiganr numero de contrato a la solcititud                
#                num_contrato = Folios.objects.filter(tipo=2).aggregate(Max('numero'))['numero__max']
#                if not num_contrato:
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
                    'num_contrato': num_contrato_str,
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

# Comentario para actualizar

class archivo_sol(ListView):
    model = Solicitud
    template_name = 'gestion/solicitud_archivo.html'
    def get_context_data(self, **kwargs):
        context = super(archivo_sol, self).get_context_data(**kwargs)
#  Proyecto
        num_proyecto = self.kwargs.get('num_proyecto',0)
        proyecto_tb = Proyecto.objects.filter(id = num_proyecto)
        context['proyecto_tb'] = proyecto_tb
        nom_proy = proyecto_tb[0].nom_proy
#  Solicitud        
        num_solicitud = self.kwargs.get('id',0)
        solicitud_tb = Solicitud.objects.filter(id = num_solicitud)
        context['solicitud_tb'] = solicitud_tb
#  Ver solicitud 
        des_permiso = '_ver_solicitud'
        variable_proy = nom_proy + des_permiso
        variable_html = "app_proy" + des_permiso
        permiso_str = "gestion." + variable_proy
        acceso = self.request.user.has_perms([permiso_str])
        context[variable_html] = acceso
        return context
