from django import forms
from django.forms.widgets import TextInput
from django.forms import ValidationError, ModelForm, Form
from . import models

class TrabajoFinalGradoCreateForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['rows'] = 5
        self.fields['equipo_de_trabajo'].widget.attrs['rows'] = 5

    class Meta:
        model = models.TrabajoFinalGrado
        fields=['nombre_trabajo' , 'descripcion', 'equipo_de_trabajo']


class GestionarTareaform(ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['planteamiento_del_problema'].widget.attrs['rows'] = 5
        self.fields['identificacion_del_problema'].widget.attrs['rows'] = 5
        self.fields['antecedentes_del_problema'].widget.attrs['rows'] = 5

    class Meta:
        model = models.TrabajoFinalGrado
        fields=['planteamiento_del_problema' , 'identificacion_del_problema', 'antecedentes_del_problema']
