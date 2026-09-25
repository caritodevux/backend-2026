from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Empleado, Cargo, Rol

class CrearEmpleadoForm(UserCreationForm):
    # Campos para la tabla Persona
    rut = forms.CharField(
        max_length=12, 
        required=True, 
        label="RUT",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'})
    )
    nombres = forms.CharField(
        max_length=100, 
        required=True, 
        label="Nombres",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellidos = forms.CharField(
        max_length=100, 
        required=True, 
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20, 
        required=False, 
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(
        required=False, 
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    # Campos para la asignación laboral en Empleado
    id_cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(), 
        required=False, 
        label="Cargo / Departamento",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    id_rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(), 
        required=True, 
        label="Rol Asignado",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    salario = forms.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        required=False, 
        label="Salario Base (CLP)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 850000'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clase CSS a los campos nativos de UserCreationForm (username, password1, password2)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class EditarEmpleadoForm(forms.ModelForm):
    # Definimos salario con decimal_places=0 y step="1" para formatear a CLP
    salario = forms.DecimalField(
        max_digits=10,
        decimal_places=0,
        required=False,
        label="Salario Base (CLP)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '1'})
    )

    class Meta:
        model = Empleado
        fields = ['id_cargo', 'id_rol', 'salario', 'activo']
        labels = {
            'id_cargo': 'Cargo / Departamento',
            'id_rol': 'Rol Asignado',
            'activo': 'Estado Activo'
        }
        widgets = {
            'id_cargo': forms.Select(attrs={'class': 'form-select'}),
            'id_rol': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convierte el valor existente a entero para omitir el .00 al cargar el formulario
        if self.instance and self.instance.salario is not None:
            self.initial['salario'] = int(self.instance.salario)