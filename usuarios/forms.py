from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import Empleado, Persona, Cargo, Rol
from .models import Empleado, Cargo, Rol

class CrearEmpleadoForm(UserCreationForm):
    # Campos para la tabla Persona
    rut = forms.CharField(max_length=12, required=True, label="RUT (ej: 12345678-9)")
    nombres = forms.CharField(max_length=100, required=True, label="Nombres")
    apellidos = forms.CharField(max_length=100, required=True, label="Apellidos")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de Nacimiento")
    
    # Campos para la asignación laboral en Empleado
    id_cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), required=False, label="Cargo / Departamento")
    id_rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True, label="Rol Asignado")
    salario = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Salario")

    class Meta:
        model = User
        fields = ['username', 'email']

class EditarEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['id_cargo', 'id_rol', 'salario', 'activo']
        labels = {
            'id_cargo': 'Cargo / Departamento',
            'id_rol': 'Rol Asignado',
            'salario': 'Salario',
            'activo': 'Estado Activo'
        }
        widgets = {
            'id_cargo': forms.Select(attrs={'class': 'form-select'}),
            'id_rol': forms.Select(attrs={'class': 'form-select'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }