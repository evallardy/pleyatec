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
            'foto_voucher',
            'estatus_pago',
        ]
        labels = {
            'id': 'Clave',
            'convenio': 'Convenio',
            'fecha_pago':'Fecha compromiso',
            'importe':'importe',
            'fecha_voucher':'Fecha de pago',
            'importe_pagado':'Importe pagado',
            'forma_pago':'Forma de pago',
            'numero_comprobante':'Número de comprobante',
            'foto_voucher':'Imagen de comprobante',
            'estatus_pago':'Estatus del pago',
        }
        widgets = {
            'importe':forms.NumberInput(),
            'importe_pagado':forms.NumberInput(),
            'fecha_voucher':DateInput(),
        }

