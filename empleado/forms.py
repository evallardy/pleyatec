from django import forms

from bien.models import ComisionAgente
from .models import Empleado

class DateInput(forms.DateInput):
    input_type = 'date'

class EmpleadoComisionForm(forms.ModelForm): 
    class Meta:
        model = ComisionAgente
        fields = [
            'proyecto_com',
            'empleado_com',
            'comision',
        ]
        labels = {
            'proyecto_com': 'Proyecto',
            'empleado_com': 'Empleado',
            'comision': 'Comisión',
        }
        widgets = { 
            'comision':forms.NumberInput(attrs={'class':'form-control'}),
        }
 
class EmpleadoForm(forms.ModelForm): 
    class Meta:
        model = Empleado
        fields = [
            'nombre',
            'paterno',
            'materno',
            'subidPersonal',
            'rfc',
            'curp',
            'fecha_nac',
            'genero',
            'estado_civil',
            'numero_seguro_social',
            'cuenta_banco',
            'banco',
            'tipo_pago',
            'calle_num',
            'colonia',
            'municipio',
            'estado',
            'codpos',
            'telefono_fijo',
            'celular',
            'correo',
            'puesto',
            'tipo_empleado',
            'area_operativa',
            'asigna_solicitud',
            'estatus_empleado',
            'usuario',
            'foto',
        ]
        labels = {
            'nombre': 'Nombre',
            'paterno': 'Paterno',
            'materno': 'Materno',
            'subidPersonal': 'Jafe',
            'rfc': 'RFC',
            'curp': 'CURP',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
            'estado_civil': 'Estado civil',
            'numero_seguro_social': 'Numero de seguridad social',
            'cuenta_banco': 'Cuenta banco',
            'banco': 'Banco de la cuenta',
            'tipo_pago': 'Tipo de pago',
            'calle_num': 'Calle / número',
            'colonia': 'Colonia',
            'municipio': 'Municipio',
            'estado': 'Estado',
            'codpos': 'Código postal',
            'telefono_fijo': 'Teléfono',
            'celular': 'Celular',
            'correo': 'Correo',
            'subidPersonal': 'Jefe',
            'tipo_empleado':'Tipo de empleado',
            'puesto':'Puesto',
            'area_operativa':'Área operativa',
            'asigna_solicitud':'Administrador',
            'estatus_personal': 'Estatus empleado',
            'foto': 'Fotogtafía empleado',
            'usuario': 'Usuario',
        }
        widgets = { 
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'paterno':forms.TextInput(attrs={'class':'form-control'}),
            'materno':forms.TextInput(attrs={'class':'form-control'}),
            'rfc':forms.TextInput(attrs={'class':'form-control'}),
            'curp':forms.TextInput(attrs={'class':'form-control'}),
            'fecha_nac': DateInput(format='%Y-%m-%d'),
            'numero_seguro_social':forms.TextInput(attrs={'class':'form-control'}),
            'cuenta_banco':forms.TextInput(attrs={'class':'form-control'}),
            'calle_num':forms.TextInput(attrs={'class':'form-control'}),
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            'municipio':forms.TextInput(attrs={'class':'form-control'}),
            'codpos':forms.NumberInput(attrs={'class':'form-control'}),
            'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
            'celular':forms.TextInput(attrs={'class':'form-control'}),
            'correo':forms.EmailInput(attrs={'class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['materno'].required = False
        self.fields['rfc'].required = False
        self.fields['curp'].required = False
        self.fields['fecha_nac'].required = False
        self.fields['numero_seguro_social'].required = False
        self.fields['cuenta_banco'].required = False
        self.fields['calle_num'].required = False
        self.fields['colonia'].required = False
        self.fields['municipio'].required = False
        self.fields['codpos'].required = False
        self.fields['telefono_fijo'].required = False
        self.fields['correo'].required = True