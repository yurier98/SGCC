"""
Settings common to all instances of the project
"""
import os
from pathlib import Path

from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'widget_tweaks',
    'bootstrap_modal_forms',
    'pwa',
    'axes',  # Axes
    'django_extensions',
    'easyaudit',
    'import_export',
    'django_cleanup.apps.CleanupConfig',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.custom_auth',
    'apps.nomenclatures',
    'apps.inventory',
    'apps.loan',
    'apps.order',
    'apps.reports',
    'apps.core',
    'apps.security',
    'apps.audit',
    'apps.notification',

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # middleware
    # 'apps.security.middleware.BlockedIPMiddleware',
    'axes.middleware.AxesMiddleware',  # Axes
    'apps.security.middleware.BlockedIPMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'apps.audit.middleware.TracingMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',

]
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
'''revisar esto '''
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGOUT_REDIRECT_URL = 'core:home'

# languages list
LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]

ADMINS = [("Admin del sitio", "admin@localhost.to"), ]

# ***********************AUTENTICACION*********************
# Esta opcion permite convertir la session serializable para q pueda obtener los grupos desde la session
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# AUTH_PROFILE_MODULE = 'apps.accounts.Profile'
AUTH_USER_MODEL = 'accounts.UserProfile'
# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',  # Axes must be first
    'apps.custom_auth.backends.MyLDAPBackend',
    'apps.custom_auth.backends.MyAuthBackend',

    # 'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# ajustar el número de intentos de inicio de sesión fallidos antes de bloquear a un usuario usando django-axes
# AXES_FAILURE_LIMIT = 4
AXES_LOCKOUT_TEMPLATE = 'error/lockout_template.html'
# SILENCED_SYSTEM_CHECKS = ['axes.W003']


# Agrega la dirección IP que deseas bloquear a la lista de bloqueo
AXES_IP_BLACKLIST = ['123.456.789.0']

# Define cuántos intentos fallidos de inicio de sesión se permiten antes de bloquear la dirección IP
AXES_FAILURE_LIMIT = 3

# Define cuánto tiempo se debe bloquear la dirección IP después de alcanzar el límite de intentos fallidos
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = 24  # Bloquea durante 24 horas

# *********************** END AUTENTICACION *********************
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
BLOCKED_IP_TEMPLATE = 'error/blocked.html'

LOGIN_REDIRECT_URL = '/order'  # Route defined in home/urls.py
# LOGOUT_REDIRECT_URL = "/"  # Route defined in home/urls.py
LOGIN_URL = reverse_lazy('login')

LOGOUT_REDIRECT_URL = '/login/'
# LOGIN_URL = '/login/'


DEFAULT_REPORT_TEMPLATE_PATH = 'apps/reports/resources/default_report_template.json'

from .pwa import *
