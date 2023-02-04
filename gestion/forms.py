from decimal import Decimal
from django import forms

from core.funciones import valida_correo
from .models import *
import re

class DateInput(forms.DateInput):
    input_type = 'date'

class Nuvole_SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'cliente',
            'asesor',
            'lote',
            'precio_lote',
            'precio_final',
            'tipo_descuento',
            'asigna_descuento',
            'porcentaje_descuento',
            'descuento',
            'modo_pago',
            'enganche',
            'cantidad_pagos',
            'importe_x_pago',
            'foto_elector_frente',
            'foto_elector_reverso',
            'foto_comprobante',
            'foto_matrimonio',
            'estatus_solicitud',
            'foto_elector_frente_cy',
            'foto_elector_reverso_cy',
            'foto_alta_shcp',
            'foto_acta_const',
            'tipo_cliente',
            'razon',
            'nombre',
            'paterno',
            'materno',
            'nombre_conyuge',
            'paterno_conyuge',
            'materno_conyuge',
            'rfc',
            'curp',
            'estado_civil',
            'regimen',
            'calle',
            'colonia',
            'codpos',
            'municipio',
            'estado',
            'celular',
            'correo',
            'total',
            'precio_x_mt',
        ]
        labels = {
            'cliente': 'Cliente',
            'asesor': 'Asesor',
            'lote': 'Lote',
            'precio_lote': 'Precio lote',
            'precio_final': 'Precio final',
            'tipo_descuento':'Tipo descto',
            'asigna_descuento':'Asigna descto',
            'porcentaje_descuento':'% de descuento',
            'descuento': 'Descuento',
            'modo_pago': 'Modo de pago',
            'enganche': 'Enganche',
            'cantidad_pagos': 'Cantidad de pagos',
            'importe_x_pago': 'Importe por pago',
            'aprobacion_gerente': 'Aprobación gerente ventas',
            'aprobacion_director': 'Aprobación Director de Desarrollo',
            'foto_elector_frente': 'INE frente cliente',
            'foto_elector_reverso': 'INE reverso cliente',
            'foto_comprobante': 'Comprobante',
            'foto_matrimonio': 'Acta de matrimonio',
            'estatus_solicitud': 'Estatus solicitud',
            'foto_elector_frente_cy': 'INE frente cónyuge',
            'foto_elector_reverso_cy': 'INE reverso cónyuge',
            'foto_alta_shcp': 'Alta SCHP',
            'foto_acta_const': 'Acta constitutiva',
            'tipo_cliente':'Tipo de cliente',
            'razon':'Razón',
            'nombre':'Nombre del cliente',
            'paterno':'Paterno del cliente',
            'materno':'Materno del cliente',
            'nombre_conyuge':'Nombre de cónyuge',
            'paterno_conyuge':'Paterno de cónyuge',
            'materno_conyuge':'Materno de cónyuge',
            'rfc':'RFC',
            'curp':'CURP',
            'estado_civil':'Estado civil',
            'regimen':'Régimen',
            'calle':'Calle y número',
            'colonia':'Colonia',
            'codpos':'Cod.Pos.',
            'municipio':'Mpio.',
            'estado':'Estado',
            'celular':'Celular',
            'correo':'Correo', 
        }
        widgets = {
            'correo':forms.EmailInput(),
        }
    def __init__(self, *args, **kwargs):
        super(Nuvole_SolicitudForm, self).__init__(*args, **kwargs)
        self.fields['precio_lote'].required = False
        self.fields['descuento'].required = False
        self.fields['asigna_descuento'].required = False
        self.fields['porcentaje_descuento'].required = False
        self.fields['nombre'].required = False
        self.fields['paterno'].required = False
        self.fields['materno'].required = False
        self.fields['nombre_conyuge'].required = False
        self.fields['paterno_conyuge'].required = False
        self.fields['materno_conyuge'].required = False
        self.fields['razon'].required = False
        self.fields['rfc'].required = False
        self.fields['curp'].required = False
        self.fields['calle'].required = False
        self.fields['colonia'].required = False
        self.fields['codpos'].required = False
        self.fields['municipio'].required = False
        self.fields['foto_elector_frente'].required = False
        self.fields['foto_elector_reverso'].required = False
        self.fields['foto_elector_frente_cy'].required = False
        self.fields['foto_elector_reverso_cy'].required = False
        self.fields['foto_matrimonio'].required = False
        self.fields['foto_comprobante'].required = False
        self.fields['foto_alta_shcp'].required = False
        self.fields['foto_acta_const'].required = False
        self.fields['celular'].required = False
        self.fields['regimen'].required = False
        self.fields['correo'].required = False
    def clean_enganche(self):
        modo_pago = self.cleaned_data.get("modo_pago")
        enganche = self.cleaned_data.get("enganche")
        precio_lote = self.cleaned_data.get("precio_lote")
        lote = self.cleaned_data.get("lote")
        cantidad_pagos = self.cleaned_data.get("cantidad_pagos")
        if lote:
            tabla_lote = Lote.objects.filter(id=lote.id)
            proyecto = tabla_lote[0].proyecto.id
            reglas = Regla.objects.filter(proyecto=proyecto)
            if modo_pago != 1:
                if enganche == 0:
                    raise forms.ValidationError('Teclea engache')
                for regla in reglas:
                    if regla.modo_pago == modo_pago and regla.mensualidades_permitidas == cantidad_pagos:
                        if regla.tipo_enganche_minimo == 1:
                            monto = regla.valor3
                        else:
                            porcentaje = regla.valor3
                            monto = (precio_lote * porcentaje) / 100
                        if enganche < monto:
                            mensaje = "Mínimo " + "{:,}".format(monto)
                            raise forms.ValidationError(mensaje)
        return enganche
    def clean_lote(self):
        lote = self.cleaned_data.get('lote')
        if lote == None:
            raise forms.ValidationError('Seleccione un bien')
        return lote
    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError('Seleccione un cliente')
        return cliente
    def clean_razon(self):
        tipo_cliente = self.cleaned_data.get('tipo_cliente')
        razon = self.cleaned_data.get('razon')
        if tipo_cliente == 1:
            if len(razon) == 0:
                raise forms.ValidationError('Teclee razón social')
        return razon
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) == 0:
            raise forms.ValidationError('Teclee nombre cliente')
        return nombre
    def clean_paterno(self):
        paterno = self.cleaned_data.get('paterno')
        if len(paterno) == 0:
            raise forms.ValidationError('Teclee paterno cliente')
        return paterno
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if len(celular) == 0:
            raise forms.ValidationError('Teclee celular cliente')
        return celular
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if len(correo) == 0:
            raise forms.ValidationError('Teclee correo cliente')
        else:
            if not valida_correo(correo):
                raise forms.ValidationError('Correo cliente inválido')
        return correo
    def clean_cantidad_pagos(self):
        modo_pago = self.cleaned_data.get('modo_pago')
        cantidad_pagos = self.cleaned_data.get('cantidad_pagos')
        if modo_pago != 1:
            if cantidad_pagos == 0:
                raise forms.ValidationError('Seleccione mensualidades')
        return cantidad_pagos
    def clean_descuento(self):
        asigna_descuento = self.cleaned_data.get('asigna_descuento')
        tipo_descuento = self.cleaned_data.get('tipo_descuento')
        descuento = self.cleaned_data.get('descuento')
        if asigna_descuento == 1 and tipo_descuento == 2:
            if descuento <= 0:
                raise forms.ValidationError('Teclea descuento')
        precio_lote = self.cleaned_data.get('precio_lote')
        porcentaje_maximo = Decimal('0.20')
        descuento_maximmo = precio_lote * porcentaje_maximo
        if descuento > descuento_maximmo:
            raise forms.ValidationError('El descuento es mayor al permitido')
        return descuento
    def clean_porcentaje_descuento(self):
        asigna_descuento = self.cleaned_data.get('asigna_descuento')
        tipo_descuento = self.cleaned_data.get('tipo_descuento')
        porcentaje_descuento = self.cleaned_data.get('porcentaje_descuento')
        if asigna_descuento == 1 and tipo_descuento == 1:
            if porcentaje_descuento <= 0:
                raise forms.ValidationError('Teclea % descuento')
        return porcentaje_descuento
    def clean_porcentaje_descuento(self):
        asigna_descuento = self.cleaned_data.get('asigna_descuento')
        tipo_descuento = self.cleaned_data.get('tipo_descuento')
        porcentaje_descuento = self.cleaned_data.get('porcentaje_descuento')
        if asigna_descuento == 1 and tipo_descuento == 1:
            if porcentaje_descuento <= 0:
                raise forms.ValidationError('Teclea % descuento')
        return porcentaje_descuento
    def clean_id_precio_lote(self):
        data = self.cleaned_data['id_precio_lote']
        return data


class Nuvole_CompromisoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'id',
            'lote',
            'cantidad_pagos',
            'modo_pago',
            'precio_lote',
            'precio_final',

            'apartado', 
            'confirmacion_apartado',
            'forma_pago_apa',
            'cuenta_apa',
            'numero_comprobante_apa',
            'foto_comprobante_apartado',

            'pago_adicional',
            'confirmacion_pago_adicional',
            'forma_pago_pa',
            'cuenta_pa',
            'numero_comprobante_pa',
            'foto_comprobante_pago_adicional',

            'estatus_solicitud',
            'num_contrato',
        ]
        labels = {
            'id': 'Clave',
            'lote':'Clave lote',
            'apartado': 'Importe',
            'confirmacion_apartado':'Depósito',
            'pago_adicional': 'Importe',
            'confirmacion_pago_adicional':'Depósito',
            'estatus_solicitud': 'Estatus solicitud',
            'foto_comprobante_pago_adicional':'Comprobante',
            'foto_comprobante_apartado':'Comprobante',
            'forma_pago_apa':'Forma pago',
            'cuenta_apa':'Cuenta',
            'numero_comprobante_apa':'Núm. comprobante',
            'forma_pago_pa':'Forma pago',
            'cuenta_pa':'Cuenta',
            'numero_comprobante_pa':'Núm. comprobante',
            'num_contrato':'Núm. contrato',
            'precio_final':'Precio final',
        }
        widgets = {
            'cuenta_pa':forms.NumberInput(),
            'cuenta_apa':forms.NumberInput(),
        }
    def __init__(self, *args, **kwargs):
        super(Nuvole_CompromisoForm, self).__init__(*args, **kwargs)
        self.fields['apartado'].required = False
        self.fields['confirmacion_apartado'].required = False
        self.fields['forma_pago_apa'].required = False
        self.fields['cuenta_apa'].required = False
        self.fields['numero_comprobante_apa'].required = False
        self.fields['pago_adicional'].required = False
        self.fields['confirmacion_pago_adicional'].required = False
        self.fields['forma_pago_pa'].required = False
        self.fields['cuenta_pa'].required = False
        self.fields['numero_comprobante_pa'].required = False
        self.fields['lote'].required = False
        self.fields['precio_lote'].required = False
        self.fields['num_contrato'].required = False
        self.fields['foto_comprobante_apartado'].required = False
        self.fields['foto_comprobante_pago_adicional'].required = False
        self.fields['modo_pago'].required = False
        self.fields['cantidad_pagos'].required = False
        

    def clean_apartado(self):
        pk = self.instance.id
        apartado_tp = self.cleaned_data.get("apartado")
        apartado = self.cleaned_data.get("apartado")
        apartado_bd = self.instance.apartado
        if apartado_bd != apartado_tp and apartado_bd == 0:
            modo_pago = self.instance.modo_pago
            precio_lote = self.instance.precio_lote
            if modo_pago == 1:
                mensualidades = 0
            else:
                mensualidades = self.instance.cantidad_pagos
            lote = self.instance.lote
            proyecto = lote.proyecto.id
            regla = Regla.objects.filter(proyecto=proyecto,modo_pago=modo_pago, mensualidades_permitidas=mensualidades)
            if regla:
                tipo_apartado_minimo = regla[0].tipo_apartado_minimo
                valor2 = regla[0].tipo_apartado_minimo
                if tipo_apartado_minimo == 1:
                    monto = regla[0].valor2
                else:
                    porcentaje = valor2
                    monto = (precio_lote * porcentaje) / 100
                if apartado_tp < monto:
                    mensaje = "Mínimo " + "{:,}".format(monto)
                    raise forms.ValidationError(mensaje)
        else:
            if apartado_tp < 0:
                raise forms.ValidationError("Debe ser positivo")
        return apartado

    def clean_confirmacion_apartado(self):
        confirmacion_apartado = self.cleaned_data.get("confirmacion_apartado")
#        apartado_tp = self.cleaned_data.get("apartado")
#        apartado_bd = self.instance.apartado
#        if apartado_bd != apartado_tp and apartado_bd == 0:
#            #  Validamos campos apartado
#            if confirmacion_apartado == 0:
#                raise forms.ValidationError("Seleccione una opción")
        return confirmacion_apartado

    def clean_forma_pago_apa(self):
        forma_pago_apa = self.cleaned_data.get("forma_pago_apa")
        apartado_tp = self.cleaned_data.get("apartado")
        apartado_bd = self.instance.apartado
        if apartado_bd != apartado_tp and apartado_bd == 0:
            #  Validamos campos forma pago apartado
            if forma_pago_apa == 0:
                raise forms.ValidationError("Seleccione una opción")
        return forma_pago_apa

    def clean_cuenta_apa(self):
        cuenta_apa = self.cleaned_data.get("cuenta_apa")
        forma_pago_apa = self.cleaned_data.get("forma_pago_apa")
        apartado_tp = self.cleaned_data.get("apartado")
        apartado_bd = self.instance.apartado
        if apartado_bd != apartado_tp and apartado_bd == 0:
            #  Validamos campos cuenta apartado
            if cuenta_apa == "" and forma_pago_apa != 3:
                raise forms.ValidationError("Tecleé cuenta")
        return cuenta_apa

    def clean_numero_comprobante_apa(self):
        numero_comprobante_apa = self.cleaned_data.get("numero_comprobante_apa")
        forma_pago_apa = self.cleaned_data.get("forma_pago_apa")
        apartado_tp = self.cleaned_data.get("apartado")
        apartado_bd = self.instance.apartado
        if apartado_bd != apartado_tp and apartado_bd == 0:
            #  Validamos campos comprobante apartado
            if numero_comprobante_apa == "" and forma_pago_apa != 3:
                raise forms.ValidationError("Tecleé núm. comprobante")
        return numero_comprobante_apa

    def clean_pago_adicional(self):
        pk = self.instance.id
        pago_adicional_tp = self.cleaned_data.get("pago_adicional")
        pago_adicional = self.cleaned_data.get("pago_adicional")
        pago_adicional_bd = self.instance.pago_adicional
        apartado = self.instance.apartado
        if pago_adicional_bd != pago_adicional_tp and pago_adicional_bd == 0:
            modo_pago = self.instance.modo_pago
            enganche = self.instance.enganche
            precio_final = self.instance.precio_final
            if modo_pago == 1:
                diferencia = precio_final - apartado - pago_adicional
                if diferencia > 0:
                    diferencia = precio_final - apartado
                    mensaje = "Debe ser " + "{:,}".format(diferencia)
                    raise forms.ValidationError(mensaje)        
            else:
                diferencia = enganche - apartado - pago_adicional
                if diferencia > 0:
                    diferencia = enganche - apartado
                    mensaje = "Debe ser " + "{:,}".format(diferencia)
                    raise forms.ValidationError(mensaje)        
        return float(pago_adicional)

    def clean_confirmacion_pago_adicional(self):
#        pago_adicional_tp = self.cleaned_data.get("pago_adicional")
#        pago_adicional_bd = self.instance.pago_adicional
        confirmacion_pago_adicional = self.cleaned_data.get("confirmacion_pago_adicional")
#        if pago_adicional_bd != pago_adicional_tp and pago_adicional_bd == 0:
#            #  Validamos campos confirmmacion pago aicional
#            if confirmacion_pago_adicional == 0:
#                raise forms.ValidationError("Seleccione una opción")
        return confirmacion_pago_adicional

    def clean_forma_pago_pa(self):
        pago_adicional_tp = self.cleaned_data.get("pago_adicional")
        pago_adicional_bd = self.instance.pago_adicional
        forma_pago_pa = self.cleaned_data.get("forma_pago_pa")
        if pago_adicional_bd != pago_adicional_tp and pago_adicional_bd == 0:
            #  Validamos campos forma pago, pago adicional
            if forma_pago_pa == 0:
                raise forms.ValidationError("Seleccione una opción")
        return forma_pago_pa

    def clean_cuenta_pa(self):
        pago_adicional_tp = self.cleaned_data.get("pago_adicional")
        pago_adicional_bd = self.instance.pago_adicional
        cuenta_pa = self.cleaned_data.get("cuenta_pa")
        forma_pago_pa = self.cleaned_data.get("forma_pago_pa")
        if pago_adicional_bd != pago_adicional_tp and pago_adicional_bd == 0:
            #  Validamos campos cuaenta pago adicional
            if cuenta_pa == "" and forma_pago_pa != 3:
                raise forms.ValidationError("Tecleé cuenta")
        return cuenta_pa

    def clean_numero_comprobante_pa(self):
        pago_adicional_tp = self.cleaned_data.get("pago_adicional")
        pago_adicional_bd = self.instance.pago_adicional
        numero_comprobante_pa = self.cleaned_data.get("numero_comprobante_pa")
        forma_pago_pa = self.cleaned_data.get("forma_pago_pa")
        if pago_adicional_bd != pago_adicional_tp and pago_adicional_bd == 0:
            #  Validamos campos comprobante pago adicional
            if numero_comprobante_pa == "" and forma_pago_pa != 3:
                raise forms.ValidationError("Tecleé comprobante")
        return numero_comprobante_pa

class Num_LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = [
            'estatus_lote',
        ]
        labels = {
            'estatus_lote': 'Estatus lote',
        }

class CompromisoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'id',
            'apartado',
            'pago_adicional',
        ]
        labels = {
            'id': 'Clave',
            'apartado': 'Apartado',
            'pago_adicional': 'Pago adicional',
        }
        widgets = {
            'apartado':forms.NumberInput(),
            'pago_adicional':forms.NumberInput(),
        }

class DatosContratoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'modo_pago',
            'fecha_contrato',
            'anio_inicio_pago',
            'mes_inicio_pago',
        ]
        labels = {
            'modo_pago': 'Modo de pago',
            'fecha_contrato': 'Fecha de contrato',
            'anio_inicio_pago': 'Año inicio pagos',
            'mes_inicio_pago': 'Mes inicio pagos',
        }
        widgets = {
            'fecha_contrato': DateInput(),
        }
        error_messages = {
            'name': {
                'max_length': ("This writer's name is too long."),
            },
        }
    def clean(self):
        if self.cleaned_data.get('fecha_contrato')==None:
            raise forms.ValidationError('Falta fecha de contrato!')
        return self.cleaned_data
