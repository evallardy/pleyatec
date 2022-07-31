from django import forms
from django.forms import ModelForm, widgets
from .models import Proyecto, Lote
from bootstrap_datepicker_plus  import  DatePickerInput ,  TimePickerInput 

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = [
            'comision_asesor',
            'comision_jefe_asesor',
        ]
        labels = {
            'comision_asesor':'Comisión asesor',
            'comision_jefe_asesor':'Comisión coordinador',
        }
        widgets = {
            'comision_asesor':forms.NumberInput(attrs={'class':'form-control'}),
            'comision_jefe_asesor':forms.NumberInput(attrs={'class':'form-control'}),
        }

class BienForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = [
            'proyecto',
            'fase',
            'manzana',
            'lote',
            'tipo_lote',
            'obs_irregular',
            'fondo',
            'frente',
            'total',
            'precio_x_mt',
            'precio',
            'esquina',
            'colindancia_norte',
            'colindancia_sur',
            'colindancia_este',
            'colindancia_oeste',
            'terraza',
            'precio_x_mt_t',
            'precio_terraza',
            'altura',
            'estacionamientos',
            'gran_total',
            'estatus_lote',
        ]
        labels = {
            'proyecto': 'Proyecto',
            'fase': 'Fase',
            'manzana': 'Manzana',
            'lote': 'Lote',
            'tipo_lote':'Tipo de lote',
            'obs_irregular':'Observación medidas',
            'fondo': 'Fondo',
            'frente': 'Frente',
            'total': 'Total de m²',
            'precio_x_mt': 'Precio por m²',
            'precio': 'Precio total',
            'esquina': 'Esquina',
            'colindancia_norte': 'Colindancia hacia el norte',
            'colindancia_sur': 'Colindancia hacia el sur',
            'colindancia_este': 'Colindancia hacia el este',
            'colindancia_oeste': 'Colindancia hacia el oeste',
            'terraza':'Metros de terraza',
            'precio_x_mt_t':'Precio m² terraza',
            'precio_terraza':'Precio terraza',
            'altura':'Altura local',
            'estacionamientos':'Estacionamientos',
            'gran_total':'Total General',
            'estatus_lote':'Estatus del lote'
        }
        widgets = {
            'manzana':forms.NumberInput(),
            'fondo':forms.NumberInput(),
            'frente':forms.NumberInput(),
            'total':forms.NumberInput(),
            'precio_x_mt':forms.NumberInput(),
            'precio':forms.NumberInput(),
            'esquina':forms.RadioSelect(),
            'tipo_lote':forms.RadioSelect(),
            'terraza':forms.NumberInput(),
            'precio_x_mt_t':forms.NumberInput(),
            'precio_terraza':forms.NumberInput(),
            'gran_total':forms.NumberInput(),
            'altura':forms.NumberInput(),
            'estacionamientos':forms.NumberInput(),
        }

