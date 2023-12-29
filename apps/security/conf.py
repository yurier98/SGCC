from django.conf import settings


settings.BLOCKED_IP_TEMPLATE = getattr(settings, "BLOCKED_IP_TEMPLATE", None)
