from django import forms
from django.forms import ModelForm, widgets
from .models import Banco

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = [
            'banco',
            'abreviacion',
            'estatus_banco',
        ]
        labels = {
            'banco': 'Nombre del banco',
            'abreviacion': 'Abreviación del banco',
            'estatus_banco': 'Estatus del banco',
        }

