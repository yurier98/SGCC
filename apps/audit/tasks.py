from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Trace
from datetime import datetime, timedelta

@shared_task
def eliminar_registros_antiguos():
   tres_meses_atras = datetime.now() - timedelta(days=90)
   Trace.objects.filter(date__lt=tres_meses_atras).delete()
