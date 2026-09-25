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
### 0. Modificación del Modelo Entidad Relación para cumplir con "No se debe crear un modelo de usuarios desde cero para la autenticación".
- **Tablas idénticas al diagrama**: Persona, Rol, Departamento y Cargo fueron estructuradas exactamente con los mismos campos y tipos de datos que een el diagrama ER.
- **Tabla USUARIO (Reemplazada)**: El diagrama exige una tabla manual con password_hash y username. Nosotros la eliminamos y la conectamos al User nativo de Django **(auth_user)**, ya que el profesor solicitó usar **django.contrib.auth**.
- **Relación de PERSONA y el Usuario**: En el diagrama, USUARIO tiene una clave foránea rut que apunta a PERSONA. *Como el User nativo de Django no permite agregar columnas nuevas directamente* (sin crear un modelo de usuario personalizado complejo), en el Paso 1 enlazamos Persona a través de la tabla Empleado. **EMPLEADO** *actúa como el pivote del sistema*, conectando a la cuenta del sistema (AUTH_USER), la persona física (PERSONA), su nivel de permisos (ROL) y su puesto dentro de la empresa (CARGO).
- **Tabla USUARIO_ROL (Simplificada)**: El diagrama muestra una tabla intermedia para asignar el rol al usuario. Para hacer el código más limpio y fácil de consultar en las vistas de Django, en el Paso 1 nos saltamos esta tabla e *incrustamos el id_rol directamente dentro de Empleado*, manteniendo la cardinalidad 1:N (un rol puede ser asignado a varios empleados).

### 1. Adaptar usuarios/models.py para integrar la autenticación nativa
Modificamos usuarios/models.py para conectar auth_user con Persona, Cargo, Rol y Empleado.

> Al comprobar, sale un error: FieldError: Unknown field(s) (id_rol) specified for Empleado indica que la clase Empleado en tu archivo usuarios/models.py no tiene definido el campo id_rol. Cuando Django inicia y lee EditarEmpleadoForm en forms.py, intenta buscar id_rol dentro de Empleado. Al no encontrarlo en la definición del modelo, la aplicación detiene su ejecución.

Actualizamos el modelo `Empleado` en. `usuarios/models.py`. Como modificamos el modelo, hay que realizar un `makemigrations` y `migrate`.

## 2. Actualizar usuarios/admin.py
El problema con el *admin.py* original es que la clase EmpleadoAdmin aún hace referencia al campo id_usuario (que usábamos en el modelo antiguo) en lugar de user y persona (que definimos para el User nativo de Django).

Se cambio:
- *search_fields*: Se cambiaron *id_usuario__username* e *id_usuario__rut__rut* por *user__username* y *persona__rut*, alineándose con la relación de Empleado hacia User y Persona.
- *get_username*: Se actualizó *obj.id_usuario.username* a *obj.user.username*.
- *admin_order_field*: Se actualizó a *user__username* para permitir ordenar por nombre de usuario en la tabla del panel de administración.

>Para corregir un error al hacer las pruebas de flujo (antes del paso 3 de este proceso), se protegeran los métodos en usuarios/admin.py agregando una verificación de obj.user y si los cargos o departamentos son nulos.

## 3. Aplicar las migraciones a la base de datos
Estos es para que se generen las tablas físicas que se vinsularan a la tabla nativa (auth_user):
- usuarios_persona
- usuarios_departamento
- usuarios_cargo
- usuarios_empleado

```
python manage.py makemigrations usuarios
python manage.py migrate
```

### 3.1 Solucionando error al migrar por registros previos
```
It is impossible to add a non-nullable field 'persona' to empleado without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
```
Este error aparece porque Django detectó que ya existen registros previos en la base de datos para la tabla Empleado, y al intentar agregar la relación obligatoria con Persona, no sabe qué valor ponerle a los empleados antiguos.

Intetaremos permitir los valores nulos de manera temporal en *usuarios/model.py*: cambiaremos un null = True y blnak = True:
- dentro del modelo Empleado, la linea persona.
- dentro del modelo Empleado, la linea user.

> [!NOTE]
> Como modificamos profundamente el modelo (eliminamos Usuario y UsuarioRol para usar auth_user), si solo tienes datos de prueba viejos en tu equipo, la alternativa más limpia es borrar el archivo db.sqlite3 y la carpeta usuarios/migrations (excepto __init__.py), y luego ejecutar makemigrations y migrate desde cero.

## 3.2 Poblar los Roles básicos (ADMIN y VENDEDOR)
Para que los formularios y las listas desplegables funcionen correctamente, necesitamos que la tabla Rol tenga al menos los perfiles base exigidos por el proyecto.

Iniciamos el servidor: `python manage.py runserver` y ingresamos a http://127.0.0.1:8000/admin/ e inicia sesión con las credenciales del superusuario.

Agregamos los Roles: ADMIN y VENDEDOR, además de borrar los roles "antiguos" (Admin, gerente y Operador). 

## 4. Formularios de Registro y Reasignación (usuarios/forms.py)
Creamos el archivo `usuarios/forms.py`y define los dos formularios ajustados a los campos exactos de tu modelo (id_cargo, id_rol, persona y user).
- `UserCreationForm`: Maneja automáticamente el cifrado y validación de la contraseña en auth_user, mientras nos permite solicitar los datos demográficos para Persona en una sola pantalla.   
- `EditarEmpleadoForm`: Permite al Administrador reasignar cargos, departamentos y roles desde la plataforma web sin acceder a /admin/.

## 5. Vistas con Control de Acceso por Rol (usuarios/views.py)
Modificamos `usuarios/views.py` y agregamos la lógica para listar, crear y editar registros según el rol.
- **Decorador** `@login_required`: Protege las vistas para que solo usuarios autenticados ingresen.   
- **Validación de rol en backend**: Si un usuario con rol VENDEDOR intenta forzar la URL /empleado/editar/1/, el servidor valida es_admin y cancela la acción devolviéndolo al dashboard.

## 6. Mapeo de Rutas (usuarios/urls.py)
Crea `usuarios/urls.py` para enlazar estas vistas con las URLs accesibles por el navegador.
- Define los identificadores (name='dashboard', name='crear_empleado') que se utilizan dentro de los botones de las plantillas HTML para navegar entre pantallas.

>Durante la primera comprobaciòn salio error, porque el archivo principal de rutas del proyecto (config/urls.py) aún no tiene enlazado el archivo usuarios/urls.py que creamos. Por eso Django solo reconoce la ruta admin/. Para solucionarlo, se vinculo las rutas de la aplicación usuarios en el archivo principal del proyecto. Se Abrio el archivo `config/urls.py` y se reemplazo parte del código.

>Además, Para hacer que la ruta raíz (/) cargue automáticamente la plataforma sin tener que escribir /login/ o /dashboard/ en la barra de direcciones, se ajusto el archivo usuarios/urls.py

## 7. Plantilla del Panel de Trabajo (usuarios/templates/usuarios/dashboard.html)
Debes crear la estructura de carpetas dentro de la app usuarios:`usuarios/templates/usuarios/`

### 7.1 Crear una plantilla base en usuarios/templates/usuarios/base.html
Aca vive la plantilla común para todas las páginas, incluyendo a barra de navegación, estilos de Bootstrap 5 y la barra de mensajes flotantes (alertas del sistema)

### 7.2 Inicio de Sesión (usuarios/templates/usuarios/login.html)
Formulario de inicio de sesión centrado.

### 7.3 Panel de Control (usuarios/templates/usuarios/dashboard.html)
Muestra la lista general de personal. Oculta o despliega acciones de modificación y registro en función del rol del usuario conectado.

### 7.4 Crear Empleado (usuarios/templates/usuarios/crear_empleado.html)
Pantalla exclusiva del Administrador para registrar cuentas de usuario y sus datos laborales/personales.

### 7.5 Editar Empleado (usuarios/templates/usuarios/editar_empleado.html)
Permite reasignar roles, cargos y cambiar el estado activo/inactivo.

## 8. Configuración global de redirecciones en settings.py
Se modifica `config/settings.py` para controlar a dónde redirigir al usuario tras iniciar o cerrar sesión.

## 9. Comprobación
1. Inicia el servidor: python manage.py runserver.
2. Dirígete a [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/).
3. Inicia sesión con una cuenta con rol ADMIN (puedes vincular tu superusuario a un registro de Empleado con Rol ADMIN desde el /admin/).
4.Comprueba que como Administrador puedes visualizar la tabla, presionar el botón "+ Crear Nuevo Empleado" y editar registros existentes.
5.Inicia sesión con un usuario con rol VENDEDOR: confirma que el botón de creación se oculta y la columna de acciones desaparece.

# Pruebas de flujo y verificación de roles
## Vincular el superusuario al rol ADMIN
1. En el panel de administración http://127.0.0.1:8000/admin/, ir a Personas y añadir una persona con tus datos. (si no borraste la base de datos, deberias ver al menos 3 personas que ya habian sido creadas).
2. En las secciones Departamentos y Cargos agrega al menos un registro de cada uno (si no borraste la base de datos, deberias ver estas secciones con elementos que ya habian sido creados)

> Salto un error al intentar entrar a Empleados. Este error ocurre porque hay algún registro antiguo en la tabla Empleado cuya columna user está vacía (None).obj.user.username if obj.user else "Sin usuario" evita que la pantalla falle si el registro Empleado carece de usuario asignado.De igual forma, get_nombre_persona valida la existencia de obj.persona.

3. Añadimos un `Empleado` en `Empleados` y selecciona la cuenta del superusuario, persona creada, id cargo e id rol de ADMIN.
4. Volvemos a http://127.0.0.1:8000/ y redirige a login (si no estabas conectado anteriormente), si funciona correctamente debes verificar que:
- Badge visible con el texto `ADMIN`.
- Presencia del botón verde `+ Crear Nuevo Empleado`.
- Columna Acciones Admin en la tabla con la opción de editar.
5. Probamos creando desde ese dashboard un "Nuevo Empleado" y registramos un `vendedor1`, asignandole el rol de `vendedor`.

> Ese código 200 en la petición POST /empleado/crear/ indica que el formulario no superó las validaciones de Django (form.is_valid() fue False). Actualizaremos el crear_empleado.html para mostrar errores

6. Probamos entrar con la cuenta de `vendedor1` al login y comprobamos que aparezca la etiqueta de vendedor y no podemos ni crear empleado ni acciones de admin.

## Probar la protección de seguridad en Backend
1. Estando autenticado como `vendedor1`, intentamos ingresar a esta url: http://127.0.0.1:8000/empleado/crear/, aparece un mensaje "Acceso no autorizado: Solo Administradores pueden registrar empleados." y tampoco puede realizar ninguna modificación.

## Probar la edición y reasignación como ADMIN
1. Ingresamos con ADMIN. Buscamos a vendedor1 y apretamos el boton "reasignar/editar". Probamos cambianado algunos valores como 'Empleado activo'. 
2. Guardamos los cambios y verificamos que los nuevos valores se reflejen en la tabla del dashboard.

>Se agrega mensaje de error en el login modificando usuarios/templates/usuarios/login.html

>Se cambia el formato del salario a clp en models.py

>Se agrega una sección para consultar la información completa del usuario conectado, se agrega una tarjeta al dashboard.

---

# Pasos seguidos para el desarrollo de la segunda prueba.

## Resumen requerimientos
### Modelos requeridos
- **Departamento**: nombre, descripcion.   
- **Cargo**: nombre, descripcion.   
- **Empleado**: rut, nombre, apellido, email, telefono, fecha_ingreso, cargo (FK a Cargo), departamento (FK a Departamento), estado (Activo/Inactivo).  
### Administrador de Django
- Registrar los tres modelos con permisos completos de CRUD.   
- Personalizar la vista de Empleado con list_display, search_fields, list_filter y ordering.   
### Control de acceso y sesión
- Toda la sección de Administración de Personal debe estar protegida para usuarios autenticados (@login_required).   
### Flujo de navegación e interfaces
1. Home Principal (/home/ o /).   
2. Gestión de Personal (/personal/).   
3. CRUD de Empleados:Listado (/personal/empleados/)   
- Registro/Crear (/personal/empleados/crear/)   
- Detalle (/personal/empleados/<id>/)   
- Modificar/Editar (/personal/empleados/<id>/editar/)   
- Eliminar con pantalla de confirmación (/personal/empleados/<id>/eliminar/)

# Avanzando sobre los construido para la evaluación 2
## 0. Modelos y migraciones (usuarios/models.py)
No necesitamos ajustar nada, porque el modelo actual es más completo que el requerimiento básico de la pauta:
- **Datos de Empleado** (RUT, Nombre, Apellido, Email, Teléfono): Los maneja tu modelo Persona vinculado a Empleado.   
- **Departamento y Cargo**: Tu modelo Cargo ya se relaciona con Departamento (id_departamento).   
- **Fecha de Ingreso y Estado**: fecha_contratacion y activo (Activo / Inactivo).   
- **Extras**: Conservamos salario_clp, Rol y la autenticación nativa User.

## 1. Configuración de rutas en usuario/urls.py
Actualizamos para que incorpore en modulo personal.

## 2. Agregar vistas en usuarios/views.py
Actualizamos y añadimos las vistas CRUD y la vista principal del módulo.

## 3. Registrar y personalizar Django Admin en usuarios/admin.py
Dado que en tu modelo los datos personales del empleado provienen de la relación Persona y el departamento proviene de Cargo, definiremos métodos helper dentro de EmpleadoAdmin para mostrar esta información de forma ordenada en las columnas del panel de administración. Se ordeno el código.

### 3.1 Verificación en Django Admin
- Iniciamos el servidor con `python manage.py runserver`.
- Abrimos `http://127.0.0.1:8000/admin/` e ingresamos como el superusuario ADMIN.
- Verificamos que en Departamentos, se vean las columnas: ID DEPARTAMENTO, NOMBRE, DESCRIPCIÓN, FECHA CREACIÓN. 
- Probamos creando un departamento de prueba " Operaciones".
- En el terminal aparece POST y en el Django Admin aparece el nuevo item.
- Verificamos en CARGOS y revisamos si se puede seleccionar el departamento creado "Operaciones" al crear un nuevo Cargo (Operador).
- Verificamos EMPLEADOS y revisamos que existan las siguientes columnas: RUT, NOMBRE COMPLETO, USUARIO, CARGO, DEPARTAMENTO y ACTIVO.
- Probar el buscador con un rut
- Confirmamos que en el panel derecho aparezcan los filtros por: Estado (activo o Inactivo), Departamento y Cargo.

## 4. Crear e integrar templates de HTML en templates/usuarios
- Creamos `gestion_personal.html`, que muestra la información del sistema y ofrece el CRUD de empleados.
- Creamos `listar_empleado.html`, que muestra el listado de trabajadores registrado en el sistema, con botones de acciòn individual: Ver detalle, Editar, Eliminar.
- Creamos `detalle_empleado.html`, que muestra la ficha tècnica y personal asociada al empleado seleccionado.
- Creamos `eliminar_empleado.html`, que es la pantalla de confirmación para eliminar.

### 4.1 Revisando la navegación de la página
```
USUARIO
│
├── Login                      ---> /login/
├── Dashboard                  ---> /dashboard/ (Vista general)
└── Mi Perfil                  ---> (Tarjeta incorporada en Dashboard)

ADMIN
│
├── Login                      ---> /login/
├── Dashboard                  ---> /dashboard/ (Con botón de acceso al módulo)
│
└── Administración de Personal ---> /personal/ (Métricas + accesos)
     │
     ├── Listado Empleados     ---> /personal/empleados/
     ├── Registrar Empleado    ---> /personal/empleados/crear/
     ├── Detalle Empleado      ---> /personal/empleados/<id>/
     ├── Editar Empleado       ---> /personal/empleados/<id>/editar/
     └── Eliminar Empleado     ---> /personal/empleados/<id>/eliminar/
```

- Antes de continuar, fue evidente establecer un mapa de navegación que tuviera sentido con una jerarquia lógica, para que el usuario sepa en que sección se encuentra
- Para cumplir con la seguridad, un usuario común jamás verá enlaces ni tablas de gestión de empleados. Si intenta ingresar escribiendo la URL manualmente (ej: /personal/empleados/), la vista en views.py lo bloqueará y lo enviará al Dashboard con un mensaje de error. 
- Además, El usuario común ve su resumen básico en el Dashboard ("Mi Perfil"), mientras que la vista "Detalle Empleado" queda como una ficha técnica individual del módulo administrativo.
- Esto significo modificar: `usuarios/views.py`, `usuarios/forms.py`, `templates/usuarios/crear_empleado.html` y `crear_empleado.html`.

## 5. Pruebas según tipo de user
### Pruebas con usuario normal (vendedor1)
- logueamos con las credenciales de vendedor1
- Aparece el dashboard con la card de información, no hay botoón de "Administración de personal"
- Para la prueba de intrusión, ingresamos copiando en el navegado la dirección `http://127.0.0.1:8000/personal/`y `http://127.0.0.1:8000/personal/empleados/` y aparece el mensaje de "Acceso denegado: Se requieren permisos de Administrador. "

### Pruebas con usuario admin (ADMIN)
- Iniciamos sesión con la cuenta ADMIN
- Verificamos que el dashboard aparacen los accesos directos al "Módulo personal"
- Comprobamos que el CRUD funcione completo:
1. Entrar al listado (/personal/empleados/).
2. Crear un nuevo empleado (/personal/empleados/crear/).
3. Ver la ficha de detalle (/personal/empleados/<id>/).
4. Editar los datos (/personal/empleados/<id>/editar/).
5. Eliminar un usuario de prueba (/personal/empleados/<id>/eliminar/).

## 6. Algunas modificaciones de UX
- Implementación de mostrar/ocultar contyraseña, modificando `crear_empleado.html`