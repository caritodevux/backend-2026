from django.db import models
from django.contrib.auth.models import User  # Usamos la tabla nativa auth_user

class Persona(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, help_text="Formato: 12345678-9")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rut} - {self.nombres} {self.apellidos}"

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True) # Ej: 'ADMIN', 'VENDEDOR'
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre_rol

""" class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='rut')
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

class UsuarioRol(models.Model):
    id_usuario_rol = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Esto evita que un usuario tenga el mismo rol asignado dos veces
        unique_together = ('id_usuario', 'id_rol') 

    def __str__(self):
        return f"Usuario: {self.id_usuario.username} - Rol: {self.id_rol.nombre_rol}"
"""
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='id_departamento', related_name='cargos')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.id_departamento.nombre}"

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    # id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, db_column='id_usuario', related_name='empleado')
    # Reemplazamos la tabla manual Usuario por el User nativo de Django
    # Agregamos null=True, blank=True
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True)
    # Le agregamos null=True, blank=True para que Django no exija un valor por defecto
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, db_column='id_cargo', related_name='empleados')
    # Campo que falta agregar en tu model:
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True, db_column='id_rol', related_name='empleados')
    fecha_contratacion = models.DateField(auto_now_add=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        # Usamos id_usuario e id_cargo porque así llamamos a los campos
        nombre_cargo = self.id_cargo.nombre if self.id_cargo else 'Sin cargo'
        nombre_rol = self.id_rol.nombre_rol if self.id_rol else 'Sin rol'
        username = self.user.username if self.user else 'Sin usuario'
        return f"Empleado: {username} | Cargo: {nombre_cargo} | Rol: {nombre_rol}"