# Proyecto original
## Origen (Clase 5) 
Se nos pidió diseñar desde cero un modelo de datos normalizado pensado para una multitienda, empresa o taller.

## Tablas que se construyeron
Se diseñaron al menos 3 o 4 tablas relacionales en models.py:
    - Departamentos (ej. Administración, Ventas, etc.).
    - Trabajadores / Usuarios.
    - Roles (para diferenciar perfiles como Administrador/Gerente vs. Vendedor/Usuario normal).
    - Personas (para almacenar los datos demográficos aislados).

## Diagrama del modelo
https://lucid.app/lucidchart/0c2ad7d8-6123-4c5c-ad84-bae70e4356a3/edit?viewport_loc=-1%2C711%2C4320%2C2261%2C0_0&invitationId=inv_b44553c7-b0a9-4914-a844-589c21b0784e

# Requerimientos a preparación a evaluación
## Tomar el proyecto con Login de Django como Base
- En lugar de crear un modelo de usuarios propio desde cero en models.py, se debe utilizar el módulo nativo de autenticación de Django (django.contrib.auth).
- Al correr las migraciones en este proyecto base, Django genera automáticamente sus tablas por defecto (como auth_user y django_session) para gestionar los inicios de sesión y el registro.

## Traer e integrar las tablas creadas anteriormente
- Una vez que el proyecto con Login y registro esté funcionando, se deben copiar e importar los modelos relacionales que diseñaron en los avances previos (como las tablas de Departamentos, Trabajadores/Usuarios y Roles) dentro del archivo models.py de este nuevo proyecto.
- Al ejecutar makemigrations y migrate, la base de datos (SQLite) incluirá tanto las tablas nativas de Django como las tablas personalizadas del proyecto.

## Lógica de negocio y control desde la interfaz
- Gestión dentro del sistema: El profesor recalcó que la administración de roles o el cambio de departamento de un trabajador no debe hacerse solo desde el /admin/, sino desde la propia plataforma web mediante vistas y plantillas HTML.
- Permisos según el usuario: Si se ingresa como Administrador/Gerente, la aplicación debe permitir modificar o reasignar el departamento/rol de los trabajadores; mientras que si ingresa un Vendedor/Usuario normal, la interfaz restringirá estas acciones y solo le permitirá visualizar la información