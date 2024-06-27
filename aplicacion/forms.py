from django import forms
from .models import Producto, Usuario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserCreationForm


class ProductoForm(forms.ModelForm):

    
    class Meta:
        model= Producto
        fields = ['nombre','precio','tipo','descripcion','imagen']



class UpdateProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = ['nombre','precio','tipo','descripcion','imagen']


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('rut', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('rut', css_class='form-group col-md-6 mb-0'),
                Column('nombre', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('apellido', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telefono', css_class='form-group col-md-6 mb-0'),
                Column('fecha_nacimiento', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Submit('submit', 'Crear usuario')
        )


class UpdateUsuarioForm(forms.ModelForm):
    
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento']


