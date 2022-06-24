from gestion.models import Solicitud

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