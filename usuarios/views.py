from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Avg
from .forms import CrearEmpleadoForm, EditarEmpleadoForm
from .models import Empleado, Persona, Cargo, Departamento, Rol

# Función auxiliar para validar rol ADMIN de forma limpia
def es_administrador(user):
    empleado = getattr(user, 'empleado', None)
    return bool(empleado and empleado.id_rol and empleado.id_rol.nombre_rol.upper() == 'ADMIN')


# 1. Home / Dashboard (Accesible para TODOS los usuarios autenticados)
@login_required
def dashboard(request):
    empleado_actual = getattr(request.user, 'empleado', None)
    es_admin = es_administrador(request.user)

    context = {
        'es_admin': es_admin,
        'empleado_actual': empleado_actual
    }

    # Si es admin, calculamos las métricas avanzadas para el Dashboard
    if es_admin:
        total_empleados = Empleado.objects.count()
        activos = Empleado.objects.filter(activo=True).count()
        inactivos = total_empleados - activos
        
        # Agregaciones salariales (solo de personal activo)
        suma_salarios = Empleado.objects.filter(activo=True).aggregate(Sum('salario'))['salario__sum'] or 0
        promedio_salario = Empleado.objects.filter(activo=True).aggregate(Avg('salario'))['salario__avg'] or 0

        # % de operabilidad activa
        porcentaje_activos = round((activos / total_empleados * 100), 1) if total_empleados > 0 else 0
        
        # Agregaciones salariales en CLP
        suma_salarios = Empleado.objects.filter(activo=True).aggregate(Sum('salario'))['salario__sum'] or 0
        promedio_salario = Empleado.objects.filter(activo=True).aggregate(Avg('salario'))['salario__avg'] or 0

        # Últimos 5 empleados registrados en la BD
        ultimos_empleados = Empleado.objects.select_related(
            'persona', 'id_cargo__id_departamento', 'id_rol'
        ).order_by('-id_empleado')[:5]

        context.update({
            'total_empleados': total_empleados,
            'activos': activos,
            'inactivos': inactivos,
            'porcentaje_activos': porcentaje_activos,
            'total_departamentos': Departamento.objects.count(),
            'total_cargos': Cargo.objects.count(),
            'total_roles': Rol.objects.count(),
            # Formateamos los números a formato de miles CLP para la vista
            'masa_salarial': f"{int(suma_salarios):,}".replace(",", "."),
            'promedio_salarial': f"{int(promedio_salario):,}".replace(",", "."),
            'ultimos_empleados': ultimos_empleados,
        })

    return render(request, 'usuarios/dashboard.html', context)


# 2. Vista Principal de "Administración de Personal" (Exclusivo ADMIN)
@login_required
def gestion_personal(request):
    if not es_administrador(request.user):
        messages.error(request, "Acceso denegado: Se requieren permisos de Administrador.")
        return redirect('dashboard')
        
    empleado_actual = getattr(request.user, 'empleado', None)
    
    # Agrupamos todo en un diccionario "context" (es más limpio)
    context = {
        'empleado_actual': empleado_actual,
        'es_admin': True,
        'total_empleados': Empleado.objects.count(),
        'empleados_activos': Empleado.objects.filter(activo=True).count(), # NUEVO
        'total_cargos': Cargo.objects.count(),
        'total_departamentos': Departamento.objects.count(),
        'total_roles': Rol.objects.count(), # NUEVO
    }
    
    return render(request, 'usuarios/gestion_personal.html', context)

# 3. Listado General de Empleados (Exclusivo ADMIN)
@login_required
def listar_empleados(request):
    if not es_administrador(request.user):
        messages.error(request, "Acceso denegado: Se requieren permisos de Administrador.")
        return redirect('dashboard')

    # Captura de parámetros desde el formulario GET
    q = request.GET.get('q', '').strip()
    cargo_id = request.GET.get('cargo', '')

    # Convertir cargo_id a entero seguro
    cargo_actual_int = int(cargo_id) if cargo_id.isdigit() else None

    # Consulta base con relaciones optimizadas
    empleados = Empleado.objects.select_related('user', 'persona', 'id_cargo__id_departamento', 'id_rol').all()

    # Filtro por texto (Nombre, Apellido, RUT o Username)
    if q:
        empleados = empleados.filter(
            Q(persona__nombres__icontains=q) |
            Q(persona__apellidos__icontains=q) |
            Q(persona__rut__icontains=q) |
            Q(user__username__icontains=q)
        )

    # Filtro por Cargo
    if cargo_actual_int:
        empleados = empleados.filter(id_cargo_id=cargo_actual_int)

    cargos = Cargo.objects.all()

    return render(request, 'usuarios/listar_empleados.html', {
        'empleados': empleados,
        'cargos': cargos,
        'busqueda_actual': q,
        'cargo_actual': cargo_id,
        'cargo_actual_int': cargo_actual_int,
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