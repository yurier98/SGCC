from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Trace
from datetime import datetime, timedelta, timezone

from easyaudit.models import RequestEvent, CRUDEvent, LoginEvent

@shared_task
def eliminar_registros_antiguos():
   tres_meses_atras = datetime.now() - timedelta(days=90)
   Trace.objects.filter(date__lt=tres_meses_atras).delete()


@shared_task
def delete_old_records():
      # Aquí va el código para eliminar los registros viejos.
      RequestEvent.objects.filter(created_at__lt=timezone.now() - timedelta(weeks=1)).delete()
