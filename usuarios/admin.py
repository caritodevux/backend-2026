from django.contrib import admin
from .models import Persona, Usuario, Rol, UsuarioRol, Departamento, Cargo, Empleado

# --- Registros básicos (Los tuyos) ---
admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(UsuarioRol)

# --- Registros avanzados para las nuevas tablas ---
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
    search_fields = ('id_usuario__username', 'id_usuario__rut__rut', 'id_cargo__nombre')

    # Métodos para mostrar datos relacionados fácilmente en el panel
    def get_username(self, obj):
        return obj.id_usuario.username
    get_username.short_description = 'Usuario'
    get_username.admin_order_field = 'id_usuario__username'

    def get_departamento(self, obj):
        return obj.id_cargo.id_departamento.nombre if obj.id_cargo else 'N/A'
    get_departamento.short_description = 'Departamento'