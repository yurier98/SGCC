from datetime import timedelta
from django.utils import timezone
# from celery import shared_task### aun no esta instalado
from .models import SystemNotification

def delete_old_notifications():
    #obtener la fecha y hora actual
    now= timezone.now()
    # calcular la fecha y hora limite, caso 5 min antes
    limit= now-timedelta(minutes=5)
    #eliminar las notificaciones creadas antes de la fecha limite
    SystemNotification.objects.filter(created_at__lt=limit).delete()
