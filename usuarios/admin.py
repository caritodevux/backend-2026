from django.contrib import admin
from .models import Persona, Usuario, Rol, UsuarioRol

# Registramos los modelos básicos
admin.site.register(Persona)
admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(UsuarioRol)

#admin admin