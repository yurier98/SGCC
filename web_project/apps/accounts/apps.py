from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    label = 'accounts'
    verbose_name = 'Cuentas de usuarios'

    def ready(self):
        from ..accounts import signals
    #     #import apps.accounts.signals
    #     #import signals
