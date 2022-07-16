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
            'cuenta':'Cuenta (ultimos 4 digs)',
        }
        widgets = {
            'fecha_voucher':DateInput(),
            'importe_pagado':forms.NumberInput(),
            'cuenta':forms.NumberInput(),
        }

