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

---

# Requerimientos a preparación a evaluación
## Tomar el proyecto con Login de Django como Base
No se debe crear un modelo de usuarios desde cero para la autenticación.
Se debe utilizar el sistema nativo de Django mediante django.contrib.auth.
Al ejecutar las migraciones iniciales, Django crea automáticamente tablas como:
- auth_user
- auth_group
- auth_permission
- django_session

Estas tablas administran el registro, autenticación, permisos y sesiones de usuario.

## Traer e integrar las tablas creadas anteriormente
- Una vez que el proyecto con Login y registro esté funcionando, se deben copiar e importar los modelos relacionales que diseñaron en los avances previos (como las tablas de Departamentos, Trabajadores/Usuarios y Roles) dentro del archivo models.py de este nuevo proyecto.
- Al ejecutar makemigrations y migrate, la base de datos (SQLite) incluirá tanto las tablas nativas de Django como las tablas personalizadas del proyecto.

## Lógica de negocio y control desde la interfaz
- Gestión dentro del sistema: El profesor recalcó que la administración de roles o el cambio de departamento de un trabajador no debe hacerse solo desde el /admin/, sino desde la propia plataforma web mediante vistas y plantillas HTML.
- Permisos según el usuario: Si se ingresa como Administrador/Gerente, la aplicación debe permitir modificar o reasignar el departamento/rol de los trabajadores; mientras que si ingresa un Vendedor/Usuario normal, la interfaz restringirá estas acciones y solo le permitirá visualizar la información

**Administrador / Gerente**
Debe poder:
- Crear trabajadores.
- Editar trabajadores.
- Cambiar roles.
- Reasignar departamentos.
- Visualizar todos los registros.

**Vendedor / Usuario normal**
Debe poder:
- Iniciar sesión.
- Visualizar información.
- Consultar sus datos.

No debe tener permisos para:
- Editar trabajadores.
- Modificar roles.
- Cambiar departamentos.
- Eliminar registros.

# Pasos realizados
## Pasos realizados en el proyecto original
1. Crear e ingresar a la carpeta raíz
2. Crear y activar el entorno virtual
```
python3 -m venv venv
```
En windows:
```
venv\Scripts\activate
```
En Mac/Linux:
```
source venv/bin/activate
```

3. Instalar Django
```
pip install django
```
Verificamos la instalación con:
```
django-admin --version
```

4. Crear el proyecto global y la aplicación
```
django-admin startproject proyecto .
python manage.py startapp usuarios
```

5. Se registro la aplicación en settings.py
```
INSTALLED_APPS = [
    ...
    'usuarios',
]
```

6. Se diseñaron los modelos y se modificor el archivo usuarios/models.py:
- Personas
- Trabajadores
- Departamentos
- Roles

7. Se generar los archivos para la migración y se aplico la migración
```
python manage.py makemigrations
python manage.py migrate
```

8. Se creo el superusuario
```
python manage.py createsuperuser
```

9. Se registraron los modelos en Django Admin (usuarios/admin.py)

10. Se corrio el server y se creo la base de datos en sql
```
python manage.py runserver 
```

11. Se verifico el funcionamiento en http://127.0.0.1:8000/admin/
En este paso se comprobo que:
Comprobar que:
- Los modelos aparecen en Django Admin.
- El superusuario puede iniciar sesión.
- Las tablas fueron creadas correctamente.

---

## Pasos realizados en segunda etapa
