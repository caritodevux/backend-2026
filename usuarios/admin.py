from django.contrib import admin
#from .models import Persona, Usuario, Rol, UsuarioRol, Departamento, Cargo, Empleado
from .models import Persona, Rol, Departamento, Cargo, Empleado

# --- Registros básicos---
""" admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(UsuarioRol) """
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
    list_display = ('id_departamento', 'nombre', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id_cargo', 'nombre', 'id_departamento')
    list_filter = ('id_departamento',)
    search_fields = ('nombre', 'id_departamento__nombre')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'get_username', 'id_cargo', 'get_departamento', 'fecha_contratacion', 'activo')
    list_filter = ('activo', 'id_cargo__id_departamento', 'id_cargo')
    search_fields = ('user__username', 'persona__rut', 'id_cargo__nombre')
    # Métodos para mostrar datos relacionados fácilmente en el panel
    # ajustados al nuevo modelo
    def get_username(self, obj):
        # Agregamos la verificación de seguridad if obj.user
        return obj.user.username if obj.user else 'Sin usuario'
    get_username.short_description = 'Usuario'
    get_username.admin_order_field = 'user__username'

    def get_departamento(self, obj):
        # Agregamos verificación por si el cargo o el departamento son nulos
        if obj.id_cargo and obj.id_cargo.id_departamento:
            return obj.id_cargo.id_departamento.nombre if obj.id_cargo else 'N/A'
    get_departamento.short_description = 'Departamento'