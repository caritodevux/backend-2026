from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrearEmpleadoForm, EditarEmpleadoForm
from .models import Empleado, Persona, Cargo, Departamento

# Función auxiliar para validar rol ADMIN de forma limpia
def es_administrador(user):
    empleado = getattr(user, 'empleado', None)
    return bool(empleado and empleado.id_rol and empleado.id_rol.nombre_rol.upper() == 'ADMIN')


# 1. Home / Dashboard (Accesible para TODOS los usuarios autenticados)
@login_required
def dashboard(request):
    empleado_actual = getattr(request.user, 'empleado', None)
    es_admin = es_administrador(request.user)

    return render(request, 'usuarios/dashboard.html', {
        'es_admin': es_admin,
        'empleado_actual': empleado_actual
    })


# 2. Vista Principal de "Administración de Personal" (Exclusivo ADMIN)
@login_required
def gestion_personal(request):
    if not es_administrador(request.user):
        messages.error(request, "Acceso denegado: Se requieren permisos de Administrador.")
        return redirect('dashboard')
        
    empleado_actual = getattr(request.user, 'empleado', None)
    total_empleados = Empleado.objects.count()
    total_cargos = Cargo.objects.count()
    total_departamentos = Departamento.objects.count()
    
    return render(request, 'usuarios/gestion_personal.html', {
        'empleado_actual': empleado_actual,
        'es_admin': True,
        'total_empleados': total_empleados,
        'total_cargos': total_cargos,
        'total_departamentos': total_departamentos,
    })


# 3. Listado General de Empleados (Exclusivo ADMIN)
@login_required
def listar_empleados(request):
    if not es_administrador(request.user):
        messages.error(request, "Acceso denegado: Se requieren permisos de Administrador.")
        return redirect('dashboard')

    empleados = Empleado.objects.select_related('user', 'persona', 'id_cargo__id_departamento', 'id_rol').all()

    return render(request, 'usuarios/listar_empleados.html', {
        'empleados': empleados,
        'es_admin': True,
    })


# 4. Vista de Detalle Individual (Exclusivo ADMIN)
@login_required
def detalle_empleado(request, empleado_id):
    if not es_administrador(request.user):
        messages.error(request, "Acceso denegado: Se requieren permisos de Administrador.")
        return redirect('dashboard')

    empleado = get_object_or_404(
        Empleado.objects.select_related('user', 'persona', 'id_cargo__id_departamento', 'id_rol'), 
        id_empleado=empleado_id
    )
    return render(request, 'usuarios/detalle_empleado.html', {
        'empleado': empleado,
        'es_admin': True
    })


# 5. Crear Empleado (Exclusivo ADMIN)
@login_required
def crear_empleado(request):
    if not es_administrador(request.user):
        messages.error(request, "Acceso no autorizado: Solo Administradores pueden registrar empleados.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CrearEmpleadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            persona = Persona.objects.create(
                rut=form.cleaned_data.get('rut'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
                email=form.cleaned_data.get('email'),
                telefono=form.cleaned_data.get('telefono'),
                fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
            )
            
            Empleado.objects.create(
                user=user,
                persona=persona,
                id_cargo=form.cleaned_data.get('id_cargo'),
                id_rol=form.cleaned_data.get('id_rol'),
                salario=form.cleaned_data.get('salario')
            )
            messages.success(request, "Empleado registrado exitosamente.")
            return redirect('listar_empleados')
    else:
        form = CrearEmpleadoForm()

    return render(request, 'usuarios/crear_empleado.html', {'form': form})


# 6. Editar Empleado (Exclusivo ADMIN)
@login_required
def editar_empleado(request, empleado_id):
    if not es_administrador(request.user):
        messages.error(request, "Acceso no autorizado: Solo Administradores pueden modificar datos.")
        return redirect('dashboard')

    empleado_target = get_object_or_404(Empleado, id_empleado=empleado_id)

    if request.method == 'POST':
        form = EditarEmpleadoForm(request.POST, instance=empleado_target)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro del empleado actualizado correctamente.")
            return redirect('listar_empleados')
    else:
        form = EditarEmpleadoForm(instance=empleado_target)

    return render(request, 'usuarios/editar_empleado.html', {
        'form': form,
        'empleado': empleado_target
    })


# 7. Eliminar Empleado con Confirmación (Exclusivo ADMIN)
@login_required
def eliminar_empleado(request, empleado_id):
    if not es_administrador(request.user):
        messages.error(request, "Acceso no autorizado: Solo Administradores pueden eliminar empleados.")
        return redirect('dashboard')

    empleado_target = get_object_or_404(Empleado, id_empleado=empleado_id)

    if request.method == 'POST':
        nombre_completo = f"{empleado_target.persona.nombres} {empleado_target.persona.apellidos}" if empleado_target.persona else "Empleado"
        
        persona = empleado_target.persona
        user = empleado_target.user
        
        empleado_target.delete()
        if persona:
            persona.delete()
        if user:
            user.delete()

        messages.success(request, f"El empleado {nombre_completo} ha sido eliminado correctamente.")
        return redirect('listar_empleados')

    return render(request, 'usuarios/eliminar_empleado.html', {
        'empleado': empleado_target
    })