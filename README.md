# SGCC
> Sistema para la Gestión del Centro Cultural en la Universidad de Ciencias Informáticas

![Django CI](https://github.com/JustShip/justshipto_core/actions/workflows/django.yml/badge.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

## Estructura de carpetas:

    .
    ├── config                      # Contiene todos los archivos de configuración
    │   ├── settings                # Contiene la configuración
    │   │   ├── base.py             # contiene las configuraciones base
    │   │   ├── develop.py          # configuración específica para desarrollo
    │   │   ├── production.py       # configuración específica para producción
    │   │   ├── staging.py          # configuración específica para staging
    │   │   └── pwa.py              # configuración específica para la compatibilidad de Aplicación web progresiva
    │   ├── asgi.py                 # configuración de despliegue asíncrono
    │   ├── wsgi.py                 # configuración de despliegue
    │   └── urls.py                 # raíz de las url del proyecto
    │ 
    ├── requirements                # carpeta que contiene los requerimientos del proyecto
    │   ├── base.txt                # requerimientos base
    │   ├── develop.txt             # requerimientos para desarrollo
    │   ├── production.txt          # requerimientos para producción
    │   ├── staging.txt             # requerimientos para staging
    │   └── test.txt                # requerimientos para testing
    ├── manage.py    
    │ 
    │ 
    ├── apps                        # carpeta contenedora de aplicaciones
    │   ├── accounts                # aplicación para gestionar cuentas
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   └── core                    # aplicación núcleo del proyecto
    │   │   ├── apps.py             
    │   │   ├── middleware.py       # middlewares del núcleo
    │   │   ├── models.py           # modelos básicos que pueden ser usados por cualquier aplicación
    │   │   └── views.py
    │   │
    │   ├── inventory                # aplicación para gestionar el inventario
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── loan                    # aplicación para gestionar los préstamos
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── order                   # aplicación para gestionar los pedidos
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── reports                # aplicación para gestionar los reportes
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── notification            # aplicación para gestionar las notificaciones y alertas
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── security                # aplicación para gestionar la seguridad del sistema
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas
    │   │
    │   ├── traces                  # aplicación para gestionar las trazas
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py           # modelos
    │   │   └── views.py            # vistas




## Instalar dependencias
Para instalar las dependencias solo debe ejecutar:

    pip install -r requirements/develop.txt

Este proyecto utiliza diferentes librerias que son necesarias instalarlas con anterioridad para su correcta ejecución.

Para poderse conectar al LDAP de la UCI necesita la libreria   **python-ldap==3.4.0**, si usted es usuario de windows necesita instalar esta libreria de forma manual
#### Para instalar esta dependencia en Windows debe moverse al directorio deploy y ejecutar:

    pip install python_ldap-3.4.0-cp38-cp38-win_amd64.whl
Esta dependencia python_ldap-3.4.0-**cp38-cp38**-win_amd64 es compatible con **python 3.8**



#### Instalar Weasyprint => es una libreria para la creación de pdf

Esta libreria se instala automaticamente con el requirements pero para los usuarios de windows necesitan instalar **GTK-for-Windows-Runtime-Environment-Installer**

https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases


## Base de datos
Este proyecto en modo desarrollo usa SQlite por lo que solo tienes que ejecutar las migraciones:

`python manage.py migrate`

Después creas un usuario administrador:

`python manage.py createsuperuser`

Rellenas toda la información que te pide y ya está listo para ejecutar:
## Ejecutar
Ejecutar el proyecto localmente

    python manage.py runserver

Abre tu navegador en http://localhost:8000 y verás el sitio ejecutándose, si está conectado a
la red UCI podrá autenticarse mendiante su usuario y contraseña usando el LDAP de la universidad 

## Cargar datos por defecto 

Una vez montado el sistema es necesario crear los grupos o Roles definidos por defecto 
en el sistema.

Este sistema tiene definido hasta el momento 2 roles: **tecnico** y **administrador**


El rol de **tecnico** tiene permisos para:
        
        'add_product',
        'change_product',
        'delete_product',
        'view_product',
        'report_product',

        'add_loan',
        'change_loan',
        'delete_loan',
        'view_loan',
        'report_loan',

        'approve_order',
        'view_all_order',
Además un usuario tecnico podrá ver en el menu los módulo: **Pedidos, Préstamos, Inventario y Reportes**

El módulo de Pedido al que tiene acceso el tecnico podrá ver todos los pedidos del sitema
pero no puede crear un pedido. 


( _**Esta informacion necesita actualizarse**_ ) El rol de **administrador** tiene permisos para acceder:

         'view_category',
### Cargar datos de los Grupos o Roles

` python manage.py loadgroups`

### Cargar datos de usuarios 

Cargar datos de usuarios de prueba para el rol administrador y tecnico 

` python manage.py loadusers`

**username**='admin' y **password**='admin'

**username**='tecnico' y **password**='tecnico'