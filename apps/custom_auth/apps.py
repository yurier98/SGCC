from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.custom_auth'
    label = 'custom_auth'
    verbose_name = 'Autorizacion'
