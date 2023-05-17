from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
import decimal
from django.forms.widgets import NumberInput
from django.core.validators import validate_email

from .models import *
import re

class DateInput(forms.DateInput):
    input_type = 'date'

class CommaSeparatedNumberInput(forms.TextInput):
    def format_value(self, value):
        if value is None:
            return ''
        # Convertir el valor a una cadena con separadores de miles
        value = '{:,.2f}'.format(value)
        # Reemplazar el punto decimal por una coma
        value = value.replace('.', ',')
        return value

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
            'credito',
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
            'credito':'Crédito',
            'asigna_descuento':'Asigna descto',
            'porcentaje_descuento':'% de descuento',
            'descuento': 'Descuento',
            'modo_pago': 'Modo pago',
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
            'nombre':'Nombre cliente',
            'paterno':'Paterno cliente',
            'materno':'Materno cliente',
            'nombre_conyuge':'Nombre cónyuge',
            'paterno_conyuge':'Paterno cónyuge',
            'materno_conyuge':'Materno cónyuge',
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
            'correo':forms.TextInput(),
            'precio_lote': forms.TextInput(attrs={'input': '99,999,999.99'}),
            'credito': forms.TextInput(attrs={'input': '99,999,999.99'}),
            'precio_final': forms.TextInput(attrs={'input': '99,999,999.99'}),
            'descuento': forms.TextInput(attrs={ 'input': '99,999,999.99'}),
            'precio_x_mt': forms.TextInput(attrs={'input': '99,999,999.99'}),
            'enganche': forms.TextInput(attrs={'input': '99,999,999.99'}),
            'importe_x_pago': forms.TextInput(attrs={'input': '99,999,999.99'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.visible_fields():
            if form.name != 'correo':
                form.field.widget.attrs['class'] = 'form-control'
                form.field.widget.attrs['autocomplete'] = 'off'
            else:
                pass
#        self.fields['cliente'].widget.attrs['autofocus'] = True

        self.fields['lote'].required = False
        self.fields['cliente'].required = False
        self.fields['precio_lote'].required = False
        self.fields['descuento'].required = False
        self.fields['credito'].required = False
        self.fields['asigna_descuento'].required = False
        self.fields['porcentaje_descuento'].required = False
        self.fields['modo_pago'].required = False
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
        self.fields['estatus_solicitud'].required = False
        self.fields['asesor'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        # Obtener valores de los campos y quitar comas
        enganche = self.data.get('enganche', None)
        if enganche is not None:
            cleaned_data['enganche'] = enganche.replace(',', '')
        precio_lote = self.data.get('precio_lote', None)
        if precio_lote is not None:
            cleaned_data['precio_lote'] = precio_lote.replace(',', '')
        precio_final = self.data.get('precio_final', None)
        if precio_final is not None:
            cleaned_data['precio_final'] = precio_final.replace(',', '')
        descuento = self.data.get('descuento', None)
        if descuento is not None:
            cleaned_data['descuento'] = descuento.replace(',', '')
        importe_x_pago = self.data.get('importe_x_pago', None)
        if importe_x_pago is not None:
            cleaned_data['importe_x_pago'] = importe_x_pago.replace(',', '')
        credito = self.data.get('credito', None)
        if credito is not None:
            cleaned_data['credito'] = credito.replace(',', '')
        return cleaned_data


    def clean_celular(self):
        cliente = self.cleaned_data.get('cliente', '' )
        celular = self.cleaned_data.get('celular', '' )
        if not cliente == '':
            if celular == None or celular.strip() == '':
                raise ValidationError('Teclea el celular del cliente')
        return celular
    def clean_correo(self):
        cliente = self.cleaned_data.get('cliente', '' )
        correo = self.cleaned_data.get('correo', '' )
        if not cliente == '':
            if correo == None or correo.strip() == '' :
                raise ValidationError('Teclea el correo del cliente')
            else:
                try:
                    validate_email(correo)
                except ValidationError:
                    raise ValidationError('El correo electrónico del cliente es inválido')
        return correo
    def clean_razon(self):
        cliente = self.cleaned_data.get('cliente', '' )
        razon = self.cleaned_data.get('razon', '' )
        if not cliente == '':
            tipo_cliente = self.cleaned_data['tipo_cliente']
            if tipo_cliente == 1: 
                if razon == None or razon.strip() == '': 
                    raise ValidationError('Teclea la razón social del cliente')
        return razon
    def clean_nombre(self):
        cliente = self.cleaned_data.get('cliente', '' )
        nombre = self.cleaned_data.get('nombre', '' )
        if not cliente == '':
            tipo_cliente = self.cleaned_data['tipo_cliente']
            if nombre == None or nombre.strip() == '':
                if tipo_cliente == 0:
                    raise ValidationError('Teclea el nombre del cliente')
                else:
                    raise ValidationError('Teclea e nombre del representante legal')
        return nombre
    def clean_paterno(self):
        cliente = self.cleaned_data.get('cliente', '' )
        paterno = self.cleaned_data.get('paterno', '' )
        if not cliente == '':
            tipo_cliente = self.cleaned_data['tipo_cliente']
            if paterno == None or paterno.strip() == '':
                if tipo_cliente == 0:
                    raise ValidationError('Teclea el paterno del cliente')
                else:
                    raise ValidationError('Teclea el nombre del representante legal')
        return paterno
    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente', '' )
        if cliente == '':
            raise ValidationError('Debes seleccionar un cliente')
        return cliente
    def clean_lote(self):
        lote = self.cleaned_data.get('lote', '' )
        if lote == '':
            raise ValidationError('Debes seleccionar un bien')
        return lote
    def clean_enganche(self):
        modo_pago = self.cleaned_data['modo_pago']
        enganche = self.cleaned_data['enganche']
        if modo_pago > 1:
            modo_pago = self.cleaned_data['modo_pago']
            cleaned_data = super().clean()
            enganche_calculado = self.data.get("enganche_calculado")
            if enganche_calculado == None:
                enganche_calculado = 0
            importe_formateado = self.data.get("importe_formateado")
            if importe_formateado == None:
                importe_formateado = 0
            if enganche <= 0 and modo_pago > 1:
                raise ValidationError('El enganche debe der mayor a cero')
            if enganche < decimal.Decimal(enganche_calculado):
                raise ValidationError('El enganche debe der mayor a ' + importe_formateado)
        return enganche
    def clean_cantidad_pagos(self):
        modo_pago = self.cleaned_data['modo_pago']
        cantidad_pagos = self.cleaned_data['cantidad_pagos']
        if modo_pago > 1:
            modo_pago = self.cleaned_data['modo_pago']
            if cantidad_pagos <= 0 and modo_pago > 1:
                raise ValidationError('Seleccione la cantidad de pagos')
        return cantidad_pagos
    def clean_porcentaje_descuento(self):
        porcentaje_descuento = self.cleaned_data['porcentaje_descuento']
        asigna_descuento = self.cleaned_data['asigna_descuento']
        tipo_descuento = self.cleaned_data['tipo_descuento']
        if asigna_descuento == 1 and tipo_descuento == 1 and porcentaje_descuento == 0:
            raise ValidationError('El porcentaje de descuento debe der mayor a 0')
        return porcentaje_descuento
    def clean_precio_lote(self):
        precio_lote = self.cleaned_data['precio_lote']
        precio_lote = precio_lote
        precio_lote = decimal.Decimal(precio_lote)
        return precio_lote
    def clean_credito(self):
        credito = self.cleaned_data['credito']
        credito = credito
        credito = decimal.Decimal(credito)
        return credito
    def clean_precio_final(self):
        precio_final = self.cleaned_data['precio_final']
        precio_final = precio_final
        precio_final = decimal.Decimal(precio_final)
        return precio_final
    def clean_descuento(self):
        descuento = self.cleaned_data['descuento']
        asigna_descuento = self.cleaned_data['asigna_descuento']
        tipo_descuento = self.cleaned_data['tipo_descuento']
        if asigna_descuento == 1 and tipo_descuento == 2 and descuento == 0:
            raise ValidationError('El descuento debe der mayor a 0')
        return descuento
    def clean_importe_x_pago(self):
        importe_x_pago = self.cleaned_data['importe_x_pago']
        if importe_x_pago == None:
            importe_x_pago = 0
        return importe_x_pago
    def save(self, commit=True):
        solicitud = self.cleaned_data
        solicitud.save()
        return solicitud

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
