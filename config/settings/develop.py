"""
This is the settings file that you use when you're working on the project locally.
Local development-specific include DEBUG mode, log level, and activation of developer tools like django-debug-toolsbar
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0nnk7ek=1k2az6c@viwosjb5v^41w)lb8ne^!uj29ih0$-16(4'

# SECURITY WARNING: don't run with debug turned on in production.py!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ["10.8.92.217", "ec2-54-528-27-21.compute-1.amazonaws.com"]

# media files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ***********************CONFIG EMAIL*********************


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.smtp2go.com'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'estudiantes.uci.cu'
EMAIL_HOST_PASSWORD = 'KoxeCSdDtVLtMc8g'

# EMAIL_HOST = 'smtp.uci.cu'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'yurierjhl@uci.cu'
# EMAIL_HOST_PASSWORD = 'password'

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# DOMAIN = ''
# *********************** END CONFIG EMAIL*********************

