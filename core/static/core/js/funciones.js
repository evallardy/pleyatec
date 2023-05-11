function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            if (key === 'lote' || key === 'cliente') {
                html += '<li>' + key.charAt(0).toUpperCase() + key.slice(1) + " : " + String(value).charAt(0).toUpperCase() + String(value).slice(1) + '</li>';
            } else {
                html += '<li>' + String(value).charAt(0).toUpperCase() + String(value).slice(1) + '</li>';
            }
        });
        html += '</ul>';
    }
    else{
        html = '<p>'+obj+'</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}
async function message_aviso(titulo, mensaje) {
    var html = '';
    if (typeof (mensaje) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(mensaje, function (key, value) {
            html += '<li>' + key.replaceAll('_',' ') + ' : ' + value + '</li>';
        });
        html += '</ul>';
    }
    else{
        html = '<p>'+mensaje+'</p>';
    }
    await Swal.fire({
        title: titulo,
        html: html,
        icon: 'success'
    });
//    await new Promise(resolve => setTimeout(resolve, 5000)); //pausa de 5 segundos
//    Swal.close();
}
function calcula_operacion(descuento, porcentaje_descuento, modo_pago, idLote, enganche, cantidad_pagos, asigna_descuento, tipo_desc) {
    url = '/gestion/calcula_operacion/' + descuento + '/' + porcentaje_descuento + '/' + modo_pago + '/' + idLote + '/' + enganche + '/' + cantidad_pagos + '/' + asigna_descuento + '/' + tipo_desc + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            $('#id_total').val(data.datos['total']);
            $('#id_precio_x_mt').val(data.datos['precio_x_mt']);
            $('#id_precio_lote').val(data.datos['precio']);
            $('#id_precio_final').val(data.datos['precio_final']);
            $('#id_credito').val(data.datos['credito']);
            $('#id_importe_x_pago').val(data.datos['pago_mensual']);
            $('#id-enganche-minimo-error').html(data.datos['error_enganche']);
            $('#id_enganche_calculado').val(data.datos['enganche_calculado']);
            $('#id_importe_formateado').val(data.datos['importe_formateado']);
            if (asigna_descuento == "1") {
                if (tipo_desc == "1") {
                    $('#id_descuento').val(data.datos['descuento']);
                } else {
                    $('#id_porcentaje_descuento').val(data.datos['porcentaje_descuento']);
                }
            } else {
                $('#id_descuento').val(data.datos['descuento']);
                $('#id_porcentaje_descuento').val(data.datos['porcentaje_descuento']);
            }
        }
    });
}
function valores_bien_inicial(id) {
    url = '/gestion/valores_bien_inicial/' + id + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            $('#id_precio_x_mt').val(data.datos['precio_x_mt']);
            $('#id_precio_lote').val(data.datos['precio']);
        }
    });
}
function valores_bien(id, importe, proyecto, modo_pago, enganche, cantidad_pagos) {
    url = '/gestion/valores_bien/' + id + '/' + importe + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(data) {
            precio = data.datos['precio'].replaceAll(',','');
            $('#id_precio_x_mt').val(data.datos['precio_x_mt']);
            $('#id_precio_lote').val(data.datos['precio']);
            $('#id_precio_final').val(data.datos['precio']);
            valida_enganche_minimo(proyecto, modo_pago, precio, enganche, cantidad_pagos);
        }
    });
}
function valida_enganche_minimo(proyecto, modo_pago, precio, enganche, mensualidades) {
    url = '/gestion/valida_enganche_minimo/' + proyecto + '/' + modo_pago + '/' + precio + '/' + enganche + '/' + mensualidades + '/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            $('#id-enganche-minimo-error').html(response.mensaje);
        }
    });
}

function descuento_credito(id) {
    $.ajax({
        url: '/paciente/datos_paciente/' + id + "/",
        type: 'GET',
        success: function(response) {
            $('#expediente-cliente').html(response);
            $('#id-nombre-paciente').val('');
            if (id == '0') {
                $('#id-celular').val($('#id-celular-memoria').val());
            }
        }
    });
}
function confirmacion(titulo, contenido, url_ok, url_nok, texto_ok, texto_nok) {
    $.confirm({
        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-green',
                action: function(){
                    document.location.href = url_ok;
                    $.alert(texto_ok);
                }
            },
            info1: {
                text: 'No',
                btnClass: 'btn-red',
                keys:['esc'],
                action: function(){
                    if (url_nok != "") {
                        document.location.href = url_nok;
                    }
                    $.alert(texto_nok);
                }
            },
        }
    });
}
function aviso(titulo, contenido) {
    $.confirm({
//        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
//        columnClass: 'small',
        autoClose: false,
//        typeAnimated: true,
//        cancelButtonClass: 'btn-primary',
//        draggable: true,
//        dragWindowBorder: false,
        buttons: {
            buttonName: {
                text: 'OK',
                btnClass: 'btn-blue',
//                keys:['esc','enter'],
            }
        }
    });
}
function cuadro(objeto_id, objeto_lb) {
    objeto_lb.removeClass("form-check-label");
    objeto_lb.after(objeto_id);
    objeto_id.removeClass("checkboxinput");
    objeto_id.removeClass("form-check-input");
    objeto_id.css("display", "block");
    objeto_id.css("text-align", "center");
    objeto_id.css("width", objeto_lb.css("width"));
//    objeto_id.css("margin-top", "5px");
    objeto_id.css("height", "25px");
}
