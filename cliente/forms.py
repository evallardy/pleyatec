from django import forms
from django.forms import DateField, ModelForm, widgets
from .models import Cliente
from bootstrap_datepicker_plus  import  DatePickerInput ,  TimePickerInput 

class DateInput(forms.DateInput):
    input_type = 'date'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_cliente',
            'razon',
            'nombre',
            'paterno',
            'materno',
            'rfc',
            'curp',
            'fecha_nac',
            'genero',
            'estado_civil',
            'calle',
            'colonia',
            'codpos',
            'municipio',
            'estado',
            'celular',
            'correo',
            'estatus_cliente',
            'asesor',
            'nombre_conyuge',
            'paterno_conyuge',
            'materno_conyuge',
        ]
        labels = {
            'tipo_cliente':'Tipo cliente',
            'razon':'Razón social',
            'nombre': 'Nombre',
            'paterno': 'Paterno',
            'materno': 'Materno',
            'rfc': 'RFC',
            'curp': 'CURP',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
            'estado_civil': 'Estado civil',
            'calle': 'Calle y número',
            'colonia': 'Colonia',
            'codpos': 'Código postal',
            'municipio': 'Municipio',
            'estado': 'Estado',
            'celular': 'Celular',
            'correo': 'Correo electrónico',
            'estatus_cliente': 'Estatus cliente',
            'asesor': 'Asesor',
            'nombre_conyuge': 'Nombre del Conyuge',
            'paterno_conyuge': 'Paterno del Conyuge',
            'materno_conyuge': 'Materno del Conyuge',
        }
        widgets = {
            'tipo_cliente':forms.RadioSelect(),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),   #   requerido
            'paterno':forms.TextInput(attrs={'class':'form-control'}),   #   requerido
            'materno':forms.TextInput(attrs={'class':'form-control'}),
            'rfc':forms.TextInput(attrs={'class':'form-control'}),
            'curp':forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nac':DateInput(format='%Y-%m-%d'),
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            'codpos':forms.NumberInput(attrs={'class':'form-control'}),
            'municipio':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
            'celular':forms.TextInput(attrs={'class':'form-control'}),           #   requerido
            'correo':forms.EmailInput(attrs={'class':'form-control'}),          #   requerido
            'nombre_conyuge':forms.TextInput(attrs={'class':'form-control'}),
            'paterno_conyuge':forms.TextInput(attrs={'class':'form-control'}),
            'materno_conyuge':forms.TextInput(attrs={'class':'form-control'}),
        }
