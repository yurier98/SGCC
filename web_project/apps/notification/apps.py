from django.apps import AppConfig


class NotificacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    #name = 'notification'
    name = 'apps.notification'
    label = 'notification'
    verbose_name = 'Notificaciones'
