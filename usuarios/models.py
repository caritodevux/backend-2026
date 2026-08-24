from django.db import models
from django.utils import timezone

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
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre_rol

class Usuario(models.Model):
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