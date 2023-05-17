from django import forms
from django.forms import DateField, ModelForm, widgets
from django.core.validators import validate_email

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
            'fecha_nac':DateInput(format='%Y-%m-%d'),
            'codpos':forms.NumberInput(attrs={'class':'form-control'}),
            'correo':forms.EmailInput(attrs={'class':'form-control'}),          #   requerido
        }
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].required = False
        self.fields['materno'].required = False
        self.fields['rfc'].required = False
        self.fields['curp'].required = False
        self.fields['fecha_nac'].required = False
        self.fields['calle'].required = False
        self.fields['colonia'].required = False
        self.fields['codpos'].required = False
        self.fields['municipio'].required = False
        self.fields['nombre_conyuge'].required = False
        self.fields['paterno_conyuge'].required = False
        self.fields['materno_conyuge'].required = False
        self.fields['correo'].required = False

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo or correo.strip() == "":
            raise forms.ValidationError('Teclee un correo')
        else:
            try:
                validate_email(correo)
            except forms.ValidationError:
                raise forms.ValidationError('El correo es inválido')
        return correo

    def clean_razon(self):
        razon = self.cleaned_data.get('razon')
        tipo_cliente = self.cleaned_data.get('tipo_cliente')
        if tipo_cliente == 0:
            razon = ""
        else:
            if not razon or razon.strip() == "":
                raise forms.ValidationError('Tecleé la razón social')
        return razon

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == "":
            raise forms.ValidationError('Tecleé nombre')
        return nombre

    def clean_paterno(self):
        paterno = self.cleaned_data.get('paterno')
        if not paterno or paterno.strip() == "":
            raise forms.ValidationError('Tecleé paterno')
        return paterno

    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not celular or celular.strip() == "":
            raise forms.ValidationError('Tecleé el número de celular')            
        else:
            celular1 = celular.replace('-', '').replace(' ', '')
            if len(celular1) < 10:
                raise forms.ValidationError('El número de celular debe tener al menos 10 dígitos numéricos')
        return celular
