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
            'subidPersdonal',
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
            'subidPersdonal': 'Jafe',
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
            'subidPersdonal': 'Jefe',
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
            'asigna_solicitud':forms.CheckboxInput(),
        }