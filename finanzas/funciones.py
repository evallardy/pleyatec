from bien.models import PagoComision
from empleado.models import Empleado
from gestion.models import Solicitud
from django.db.models.aggregates import Count
from django.db.models import Sum

def datos_tabla_amortizacion(pk):

    solicitud = Solicitud.objects.filter(id=pk).first()
    # Precio final
    field_object = Solicitud._meta.get_field('precio_final')
    precio_final = field_object.value_from_object(solicitud)
    # Enganche
    field_object = Solicitud._meta.get_field('enganche')
    enganche = field_object.value_from_object(solicitud)
    # Importe por pagar a crÃ©dito
    impPorPagar = precio_final - enganche
    # Importe por pago
    field_object = Solicitud._meta.get_field('importe_x_pago')
    importe_x_pago = field_object.value_from_object(solicitud)
    # Cantidad de pagos
    field_object = Solicitud._meta.get_field('cantidad_pagos')
    cantidad_pagos = field_object.value_from_object(solicitud)

    interes = 0  ##  interes mensual a cada pago
    interes_total = impPorPagar * interes / 100
    pago_total = impPorPagar + interes_total
    # Columna 2
    saldo_inicial = impPorPagar + interes_total
    # Columna 3
    pago_mensual = importe_x_pago
    # Columna 4
    interes_mensual = importe_x_pago * interes / 100
    # Columna 5
    pago_total_mensual = pago_mensual + interes_mensual
    # Columna 6
    saldo_final = saldo_inicial - pago_total_mensual
    # Saldos
    saldo_capital = impPorPagar - importe_x_pago
    saldo_interes = interes_total - interes_mensual
    datos = {}
    datos['titulo'] = []
    datos['titulo'].append({
        'precio_final': precio_final,
        'enganche': enganche,
        'impPorPagar': impPorPagar,
        'importe_x_pago': importe_x_pago,
        'cantidad_pagos': cantidad_pagos,
        'interes': interes,
        'interes_total': interes_total,
        'pago_total': pago_total,
        'pk': pk,})
    datos['pagos'] = []
    for i in range(0,cantidad_pagos,1):
        datos['pagos'].append({
            'pago': i + 1,
            'saldo_inicial': saldo_inicial,
            'pago_mensual': pago_mensual,
            'interes_mensual': interes_mensual,
            'pago_total_mensual': pago_total_mensual,
            'saldo_final': saldo_final})
        # Columna 2
        saldo_inicial = saldo_final
        # Columna 3
        if saldo_capital < importe_x_pago:
            pago_mensual = saldo_capital
        # Columna 4
        if saldo_interes < interes_mensual:
            interes_mensual = saldo_interes
        # Columna 5
        pago_total_mensual = pago_mensual + interes_mensual
        # Columna 6
        saldo_final = saldo_inicial - pago_total_mensual

        saldo_capital -= pago_mensual
        saldo_interes -= interes_mensual
    return datos

def datos_comisiones_concentrado(num_proyecto, fecha_desde, fecha_hasta, estatus):
    if estatus == 0:  #  Nuevo periodo de pago
        ##  ok
        registros = PagoComision.objects \
            .filter(fecha_contrato__range=[fecha_desde, fecha_hasta], proyecto_pago=num_proyecto, \
                estatus_comision=0) \
            .values('proyecto_pago') \
            .annotate(bienes=Count('bien_pago'),total_asesor=Sum('importe'), \
            total_gerente=Sum('importe_gerente'),total_publicidad=Sum('importe_publicidad'))
    else:
        ##  ok
        registros = PagoComision.objects \
            .filter(fecha_periodo=fecha_desde, proyecto_pago=num_proyecto, estatus_comision=estatus) \
            .values('proyecto_pago') \
            .annotate(bienes=Count('bien_pago'),total_asesor=Sum('importe'), \
            total_gerente=Sum('importe_gerente'),total_publicidad=Sum('importe_publicidad'))
    return registros


def datos_comision_detalle_concentrado(opcion, num_proyecto, fecha_desde, fecha_hasta, estatus):
    if estatus == 0:  #  Nuevo periodo de pago
        if opcion == 1:   #  Detalle Asesores 
            ###  ok
            registros = Empleado.objects \
                .filter(pagocomision__fecha_contrato__range=[fecha_desde, fecha_hasta], pagocomision__proyecto_pago=num_proyecto,) \
                .values('pagocomision__asesor_pago','pagocomision__estatus_pago_asesor','nombre','paterno','materno') \
                .annotate(bienes=Count('pagocomision__bien_pago'),total_asesor=Sum('pagocomision__importe'), \
                total_gerente=Sum('pagocomision__importe_gerente'),total_publicidad=Sum('pagocomision__importe_publicidad')) \
                .order_by('pagocomision__gerente_pago') 
        elif opcion == 2:  # Detalle gerentes
            ###  ok  
            registros = PagoComision.objects \
                    .filter(fecha_contrato__range=[fecha_desde, fecha_hasta], proyecto_pago=num_proyecto,) \
                    .values('gerente_pago','gerente_pago__nombre', 'gerente_pago__paterno','gerente_pago__materno') \
                    .annotate(bienes=Count('bien_pago'),total_asesor=Sum('importe_gerente'),) \
                    .order_by('gerente_pago') 
        elif opcion == 3:  # Detalle todo
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_contrato__range=[fecha_desde, fecha_hasta], proyecto_pago=num_proyecto,) \
                .values('proyecto_pago') \
                .annotate(bienes=Count('bien_pago'),total_publicidad=Sum('importe_publicidad'),)
        else:
            registros = PagoComision.objects.filter(id=0)
    else:
        if opcion == 1:   #  Detalle Asesores 
            ###  ok
            registros = Empleado.objects \
                .filter(pagocomision__fecha_periodo=fecha_desde, pagocomision__proyecto_pago=num_proyecto,) \
                .values('pagocomision__asesor_pago','pagocomision__estatus_pago_asesor','nombre','paterno','materno') \
                .annotate(bienes=Count('pagocomision__bien_pago'),total_asesor=Sum('pagocomision__importe'), \
                total_gerente=Sum('pagocomision__importe_gerente'),total_publicidad=Sum('pagocomision__importe_publicidad')) \
                .order_by('paterno','materno','nombre') 
        elif opcion == 2:  # Detalle gerentes
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_periodo=fecha_desde, proyecto_pago=num_proyecto,) \
                .values('gerente_pago','gerente_pago__nombre', 'gerente_pago__paterno','gerente_pago__materno') \
                .annotate(bienes=Count('bien_pago'),total_asesor=Sum('importe_gerente'),) \
                .order_by('gerente_pago__paterno','gerente_pago__materno', 'gerente_pago__nombre') 
        elif opcion == 3:  # Detalle todo
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_periodo=fecha_desde, proyecto_pago=num_proyecto,) \
                .values('estatus_pago_publicidad') \
                .annotate(bienes=Count('bien_pago'),total_publicidad=Sum('importe_publicidad'),)
        else:
            registros = PagoComision.objects.filter(id=0)
    return registros

def datos_comision_detalle(opcion, num_proyecto, fecha_desde, fecha_hasta, estatus, empleado):
    if estatus == 0:
        if opcion == 1:   #  Detalle Asesores 
            ###  ok
            registros = Empleado.objects \
                .filter(pagocomision__fecha_contrato__range=[fecha_desde, fecha_hasta], pagocomision__proyecto_pago=num_proyecto, \
                    pagocomision__estatus_comision=estatus, pagocomision__asesor_pago=empleado) \
                .order_by('-pagocomision__fecha_contrato')
        elif opcion == 2:  # Detalle gerentes
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_contrato__range=[fecha_desde, fecha_hasta], proyecto_pago=num_proyecto, \
                    estatus_comision=estatus, gerente_pago=empleado) \
                .order_by('-fecha_contrato')
        elif opcion == 3:  # Detalle todo
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_contrato__range=[fecha_desde, fecha_hasta], proyecto_pago=num_proyecto, \
                    estatus_comision=estatus) \
                .order_by('-fecha_contrato')
        else:
            registros = PagoComision.objects.filter(id=0)
    else:
        if opcion == 1:   #  Detalle Asesores 
            ###  ok
            registros = Empleado.objects \
                .filter(pagocomision__fecha_periodo=fecha_desde, pagocomision__proyecto_pago=num_proyecto, \
                    pagocomision__estatus_comision=estatus, pagocomision__asesor_pago=empleado) \
                .order_by('-pagocomision__fecha_contrato')
        elif opcion == 2:  # Detalle gerentes
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_periodo=fecha_desde, proyecto_pago=num_proyecto, \
                    estatus_comision=estatus, gerente_pago=empleado) \
                .order_by('-fecha_contrato')
        elif opcion == 3:  # Detalle todo
            ###  ok
            registros = PagoComision.objects \
                .filter(fecha_periodo=fecha_desde, proyecto_pago=num_proyecto, \
                    estatus_comision=estatus) \
                .order_by('-fecha_contrato')
        else:
            registros = PagoComision.objects.filter(id=0)
    return registros


