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



## Ejecutar
Ejecutar el proyecto localmente
### Instalar dependencias
Para instalar las dependencias solo debe ejecutar:

    pip install -r requirements/develop.txt

Este proyecto para poderse conectar al LDAP de la UCI necesita la libreria  
**python-ldap==3.4.0**, si usted es usuario de windows necesita instalar esta libreria de forma manual
#### Para instalar esta dependencia en Windows debe moverse al directorio deploy y ejecutar:

    pip install python_ldap-3.4.0-cp38-cp38-win_amd64.whl
Esta dependencia python_ldap-3.4.0-**cp38-cp38**-win_amd64 es compatible con **python 3.8**

### Base de datos
Este proyecto en modo desarrollo usa SQlite por lo que solo tienes que ejecutar las migraciones:

    python manage.py migrate
Después creas un usuario administrador:

    python manage.py createsuperuser
Rellenas toda la información que te pide y ya está listo para ejecutar:

    python manage.py runserver
Abre tu navegador en http://localhost:8000 y verás el sitio ejecutándose
