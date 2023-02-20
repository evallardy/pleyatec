from cmath import isnan
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'id',
            'convenio',
            'fecha_pago',
            'importe',
            'fecha_voucher',
            'importe_pagado',
            'forma_pago',
            'numero_comprobante',
            'file_comprobante',
            'estatus_pago',
            'deposito',
            'pagado_vencido',
            'cuenta',
        ]
        labels = {
            'id': 'Clave',
            'convenio': 'Convenio',
            'fecha_pago':'Fecha compromiso',
            'importe':'importe',
            'fecha_voucher':'Fecha comprobante',
            'importe_pagado':'Importe pagado',
            'forma_pago':'Forma de pago',
            'numero_comprobante':'Número de comprobante',
            'file_comprobante':'Archivo comprobante',
            'estatus_pago':'Estatus del pago',
            'deposito':'Depósito',
            'pagado_vencido':'Pagado',
            'cuenta':'Cuenta (4 dígitos)',
        }
        widgets = {
            'fecha_voucher':DateInput(),
            'cuenta': forms.NumberInput(),
        }
    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        self.fields['numero_comprobante'].required = False
        self.fields['convenio'].required = False
        self.fields['file_comprobante'].required = False
        self.fields['cuenta'].required = False
        self.fields['deposito'].required = False
        self.fields['forma_pago'].required = False
        self.fields['estatus_pago'].required = False
        self.fields['importe'].required = False
        self.fields['fecha_voucher'].required = False
        self.fields['importe_pagado'].required = False

    def clean_fecha_voucher(self):
        fecha_voucher = self.cleaned_data.get("fecha_voucher")
        if not fecha_voucher:
            raise forms.ValidationError('Teclea fecha de comprobante')
        return fecha_voucher

    def clean_importe_pagado(self):
        importe = self.cleaned_data.get("importe")
        importe_pagado = self.cleaned_data.get("importe_pagado")
        if importe_pagado:
            if importe > importe_pagado:
                raise forms.ValidationError('Menor a mensualidad')
        else:
            raise forms.ValidationError('Tecleé mensualidad')
        return importe_pagado

    def clean_forma_pago(self):
        forma_pago = self.cleaned_data.get("forma_pago")
        if forma_pago:
            if forma_pago < 1:
                raise forms.ValidationError('Seleccione forma pago')
        else:
            raise forms.ValidationError('Seleccione forma pago')
        return forma_pago

    def clean_cuenta(self):
        cuenta = self.cleaned_data.get("cuenta")
        forma_pago = self.cleaned_data.get("forma_pago")
        if forma_pago:
            if forma_pago > 0:
                if forma_pago != 3:
                    if not cuenta:
                        raise forms.ValidationError('Tecleé cuenta')
        else:
            raise forms.ValidationError('Tecleé cuenta')
        return cuenta

    def clean_numero_comprobante(self):
        numero_comprobante = self.cleaned_data.get("numero_comprobante")
        forma_pago = self.cleaned_data.get("forma_pago")
        if forma_pago:
            if forma_pago > 0:
                if numero_comprobante.strip() == "" and forma_pago != 3:
                    raise forms.ValidationError('Tecleé comprobante')
        else:
            raise forms.ValidationError('Tecleé comprobante')
        return numero_comprobante

