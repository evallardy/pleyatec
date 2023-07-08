from django import forms
from django.forms import ModelForm, widgets
from bien.models import Proyecto, Lote
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
            'comision_jefe_asesor':'Comisión gerente',
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
            'nivel',
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
            'precio_total',
            'estatus_lote',
        ]
        labels = {
            'proyecto': 'Proyecto',
            'fase': 'Fase',
            'manzana': 'Manzana',
            'lote': 'Lote',
            'nivel': 'Nivel',
            'tipo_lote':'Tipo de lote',
            'obs_irregular':'Observación medidas',
            'fondo': 'Fondo',
            'frente': 'Frente',
            'total': 'Total de m²',
            'precio_x_mt': 'Precio por m²',
            'precio': 'Precio',
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
            'gran_total':'Total m²',
            'precio_total':'Precio total',
            'estatus_lote':'Estatus del lote'
        }
        widgets = {
            'manzana':forms.NumberInput(),
            'fondo':forms.NumberInput(),
            'frente':forms.NumberInput(),
            'nivel':forms.NumberInput(),
            'total':forms.NumberInput(),
            'precio_x_mt':forms.NumberInput(),
            'precio':forms.NumberInput(),
            'esquina':forms.RadioSelect(),
            'tipo_lote':forms.RadioSelect(),
            'terraza':forms.NumberInput(),
            'precio_x_mt_t':forms.NumberInput(),
            'precio_terraza':forms.NumberInput(),
            'gran_total':forms.TextInput(),
            'altura':forms.NumberInput(),
            'estacionamientos':forms.NumberInput(),
        }

class FormaBien(forms.ModelForm):
    class Meta:
        model = Lote
        fields = [
            'proyecto',
            'fase',
            'manzana',
            'lote',
            'gpo_lote',
            'nivel',
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
            'precio_total',
            'estatus_lote',
        ]
        labels = {
            'gpo_lote': 'Edificio',
        }
    def __init__(self, *args, **kwargs):
        super(FormaBien, self).__init__(*args, **kwargs)
        self.fields['fase'].required = False
        self.fields['manzana'].required = False
        self.fields['lote'].required = False
        self.fields['gpo_lote'].required = False
        self.fields['nivel'].required = False
        self.fields['tipo_lote'].required = False
        self.fields['obs_irregular'].required = False
        self.fields['precio_x_mt'].required = False
        self.fields['precio_x_mt_t'].required = False
        self.fields['altura'].required = False
        self.fields['gran_total'].required = False
        self.fields['precio_total'].required = False
        self.fields['frente'].required = False
        self.fields['fondo'].required = False
        self.fields['esquina'].required = False
        self.fields['estacionamientos'].required = False
        
    def clean_fase(self):
        fase = self.cleaned_data.get('fase')
        proyecto = self.cleaned_data.get('proyecto')
        if proyecto.id == 1:
            if not validaNumero(fase):
                raise forms.ValidationError('Selecciona una fase')
        return fase
    def clean_manzana(self):
        manzana = self.cleaned_data.get('manzana')
        proyecto = self.cleaned_data.get('proyecto')
        if proyecto.id == 1:
            if not validaNumero(manzana):
                raise forms.ValidationError('Teclear númeno de manzana')
        return manzana
    def clean_lote(self):
        lote = self.cleaned_data.get('lote')
        proyecto = self.cleaned_data.get('proyecto')
        datos = Proyecto.objects.filter(id=proyecto.id, proyecto=proyecto).first()
        if not validaCadena(lote):
            raise forms.ValidationError('Teclear númeno de ' + datos.singular)
        return lote
    def clean_obs_irregular(self):
        tipo_lote = self.cleaned_data.get('tipo_lote')
        obs_irregular = self.cleaned_data.get('obs_irregular')
        proyecto = self.cleaned_data.get('proyecto')
        if proyecto.id == 1 and tipo_lote == 0:
            if not validaNumero(obs_irregular):
                raise forms.ValidationError('Teclear las medidas de bien')
        return obs_irregular
    def clean_total(self):
        total = (self.cleaned_data.get('total'))
        if not validaNumero(total):
            raise forms.ValidationError('Teclear area')
        return total
    def clean_precio_x_mt(self):
        precio_x_mt = (self.cleaned_data.get('precio_x_mt'))
        if not validaNumero(precio_x_mt):
            raise forms.ValidationError('Teclear precio m²')
        return precio_x_mt

'''
    fase = forms.DecimalField(
        label="Fase",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_fase',
                'required': 'required',
            }
        )
    )   
    lote = forms.DecimalField(
        label="# Bien",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_lote',
                'required': 'required',
            }
        )
    )   
    tipo_lote = forms.DecimalField(
        label="Tipo bien",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_tipo_lote',
                'required': 'required',
            }
        )
    )   
    obs_irregular = forms.DecimalField(
        label="Medidas",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_obs_irregular',
                'required': 'required',
            }
        )
    )   
    total = forms.DecimalField(
        label="Bien m²",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_total',
                'required': 'required',
            }
        )
    )   
    precio_x_mt = forms.DecimalField(
        label="Precio bien m²",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_precio_x_mt',
                'required': 'required',
            }
        )
    )   
    precio = forms.DecimalField(
        label="Precio bien",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_precio',
                'required': 'required',
            }
        )
    )   
    terraza = forms.DecimalField(
        label="Terraza m²",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_terraza',
                'required': 'required',
            }
        )
    )   
    precio_x_mt_t = forms.DecimalField(
        label="Precio terraza m²",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_precio_x_mt_t',
                'required': 'required',
            }
        )
    )   
    precio_terraza = forms.DecimalField(
        label="Precio terraza",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_precio_terraza',
                'required': 'required',
            }
        )
    )   
    gran_total = forms.DecimalField(
        label="Total m²",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_gran_total',
                'required': 'required',
            }
        )
    )   
    precio_total = forms.DecimalField(
        label="Precio total bien",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_precio_total',
                'required': 'required',
            }
        )
    )   
    estacionamientos = forms.DecimalField(
        label="Estacionamientos",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_estacionamientos',
                'required': 'required',
            }
        )
    )   
    colindancia_norte = forms.DecimalField(
        label="Colindancia norte",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_colindancia_norte',
                'required': 'required',
            }
        )
    )   
    colindancia_sur = forms.DecimalField(
        label="Colindancia sur",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_colindancia_sur',
                'required': 'required',
            }
        )
    )   
    colindancia_este = forms.DecimalField(
        label="Colindancia este",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_colindancia_este',
                'required': 'required',
            }
        )
    )   
    colindancia_oeste = forms.DecimalField(
        label="Colindancia oeste",
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id':'id_colindancia_oeste',
                'required': 'required',
            }
        )
    )   
'''    

def validaNumero(campo):
    if campo:
        if campo > 0:
            return True
    return False

def validaCadena(campo):
    if campo:
        if campo.strip() != "":
            return True
    return False

class FormaBienValida(forms.ModelForm):
    class Meta:
        model = Lote
        fields = [
            'proyecto',
            'fase',
            'manzana',
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
            'precio_total',
            'estatus_lote',
        ]
