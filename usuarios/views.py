from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrearEmpleadoForm, EditarEmpleadoForm
from .models import Empleado, Persona

@login_required
def dashboard(request):
    empleado_actual = getattr(request.user, 'empleado', None)
    
    # Verificamos si el usuario activo tiene rol ADMIN
    es_admin = empleado_actual and empleado_actual.id_rol.nombre_rol.upper() == 'ADMIN'
    
    # Consultamos los empleados optimizando las consultas SQL
    empleados = Empleado.objects.select_related('user', 'persona', 'id_cargo__id_departamento', 'id_rol').all()

    return render(request, 'usuarios/dashboard.html', {
        'empleados': empleados,
        'es_admin': es_admin,
        'empleado_actual': empleado_actual
    })

@login_required
def crear_empleado(request):
    empleado_actual = getattr(request.user, 'empleado', None)
    es_admin = empleado_actual and empleado_actual.id_rol.nombre_rol.upper() == 'ADMIN'
    
    # Control de seguridad en servidor
    if not es_admin:
        messages.error(request, "Acceso no autorizado: Solo Administradores pueden registrar empleados.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CrearEmpleadoForm(request.POST)
        if form.is_valid():
            # 1. Guardar User
            user = form.save()
            
            # 2. Guardar Persona
            persona = Persona.objects.create(
                rut=form.cleaned_data.get('rut'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
                email=form.cleaned_data.get('email'),
                telefono=form.cleaned_data.get('telefono'),
                fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
            )
            
            # 3. Guardar Empleado vinculando las claves foráneas
            Empleado.objects.create(
                user=user,
                persona=persona,
                id_cargo=form.cleaned_data.get('id_cargo'),
                id_rol=form.cleaned_data.get('id_rol'),
                salario=form.cleaned_data.get('salario')
            )
            messages.success(request, "Empleado registrado exitosamente.")
            return redirect('dashboard')
    else:
        form = CrearEmpleadoForm()

    return render(request, 'usuarios/crear_empleado.html', {'form': form})

@login_required
def editar_empleado(request, empleado_id):
    empleado_actual = getattr(request.user, 'empleado', None)
    es_admin = empleado_actual and empleado_actual.id_rol.nombre_rol.upper() == 'ADMIN'
    
    # Control de seguridad en servidor
    if not es_admin:
        messages.error(request, "Acceso no autorizado: Solo Administradores pueden modificar datos.")
        return redirect('dashboard')

    empleado_target = get_object_or_404(Empleado, id_empleado=empleado_id)

    if request.method == 'POST':
        form = EditarEmpleadoForm(request.POST, instance=empleado_target)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro del empleado actualizado correctamente.")
            return redirect('dashboard')
    else:
        form = EditarEmpleadoForm(instance=empleado_target)

    return render(request, 'usuarios/editar_empleado.html', {
        'form': form,
        'empleado': empleado_target
    })