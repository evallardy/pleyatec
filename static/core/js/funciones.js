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
        theme: 'Material',
        title: titulo,
        icon: 'fa fa-info',
        content: contenido,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'OK',
                btnClass: 'btn-green',
                keys:['esc','enter']
            }
        }
    });
}
