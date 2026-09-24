from django.contrib import admin
from .models import Persona, Rol, Departamento, Cargo, Empleado

# --- Registros básicos ---
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'email', 'telefono')
    search_fields = ('rut', 'nombres', 'apellidos')

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre_rol', 'descripcion')

# --- Registros avanzados para las tablas ---
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('id_departamento', 'nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id_cargo', 'nombre', 'id_departamento')
    list_filter = ('id_departamento',)
    search_fields = ('nombre', 'id_departamento__nombre')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    # Campos visibles en la lista exigidos por EVA2 (RUT, Nombre, Cargo, Depto, Estado)
    list_display = ('id_empleado', 'get_rut', 'get_nombre_completo', 'get_username', 'id_cargo', 'get_departamento', 'activo')
    
    # Filtros por Estado (activo), Departamento y Cargo
    list_filter = ('activo', 'id_cargo__id_departamento', 'id_cargo')
    
    # Búsqueda por RUT, Nombre, Apellido y Username
    search_fields = ('persona__rut', 'persona__nombres', 'persona__apellidos', 'user__username', 'id_cargo__nombre')
    
    # Ordenamiento por apellidos y nombres
    ordering = ('persona__apellidos', 'persona__nombres')

    # Métodos con formato clásico y validaciones anti-None
    def get_rut(self, obj):
        return obj.persona.rut if obj.persona else 'N/A'
    get_rut.short_description = 'RUT'
    get_rut.admin_order_field = 'persona__rut'

    def get_nombre_completo(self, obj):
        if obj.persona:
            return f"{obj.persona.nombres} {obj.persona.apellidos}"
        return 'Sin Persona'
    get_nombre_completo.short_description = 'Nombre Completo'
    get_nombre_completo.admin_order_field = 'persona__nombres'

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Sin usuario'
    get_username.short_description = 'Usuario'
    get_username.admin_order_field = 'user__username'

    def get_departamento(self, obj):
        if obj.id_cargo and obj.id_cargo.id_departamento:
            return obj.id_cargo.id_departamento.nombre
        return 'N/A'
    get_departamento.short_description = 'Departamento'
    get_departamento.admin_order_field = 'id_cargo__id_departamento__nombre'