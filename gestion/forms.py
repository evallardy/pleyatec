from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class Nuvole_SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'id',
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
        ]
        labels = {
            'id': 'Clave',
            'cliente': 'Cliente',
            'asesor': 'Asesor',
            'lote': 'Lote',
            'precio_lote': 'Precio lote',
            'precio_final': 'Precio final',
            'tipo_descuento':'Tipo de descuento',
            'asigna_descuento':'Asigna descuento',
            'porcentaje_descuento':'% de descuento',
            'descuento': 'Descuento',
            'modo_pago': 'Modo de pago',
            'enganche': 'Enganche',
            'cantidad_pagos': 'Cantidad de pagos',
            'importe_x_pago': 'Importe por pago',
            'aprobacion_gerente': 'Aprobación gerente ventas',
            'aprobacion_director': 'Aprobación director de desarrollo',
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
            'precio_lote':forms.NumberInput(),
            'precio_final':forms.NumberInput(),
            'tipo_descuento':forms.RadioSelect(),
            'porcentaje_descuento':forms.NumberInput(),
            'descuento':forms.NumberInput(),
            'enganche':forms.NumberInput(),
            'cantidad_pagos':forms.NumberInput(),
            'importe_x_pago':forms.NumberInput(),
            'aprobacion_gerente':forms.CheckboxInput(),
            'aprobacion_director':forms.CheckboxInput(),
            'asigna_descuento':forms.RadioSelect(),
            'correo':forms.EmailInput(),
        }

class Nuvole_CompromisoForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'id',
            'lote',
            'apartado',
            'confirmacion_apartado',
            'pago_adicional',
            'confirmacion_pago_adicional',
            'estatus_solicitud',
            'foto_comprobante_pago_adicional',
            'foto_comprobante_apartado',
            'forma_pago_apa',
            'cuenta_apa',
            'numero_comprobante_apa',
            'forma_pago_pa',
            'cuenta_pa',
            'numero_comprobante_pa',
            'num_contrato',
            'precio_final',
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
            'apartado':forms.NumberInput(),
            'pago_adicional':forms.NumberInput(),
            'cuenta_pa':forms.NumberInput(),
            'cuenta_apa':forms.NumberInput(),
        }


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