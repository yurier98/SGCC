# Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal

# from apps.order.models import Order

from .models import Order, OrderProduct

# save_loan = Signal()
from ..notification.signals import notificar


def notify_order(sender, instance, created, **kwargs):
    notificar.send(instance.user, destiny=instance.user, verb='Se ha creado un pedido a su usuario exitosamente. desde signals ',
                   level='info')

# post_save.connect(notify_order, sender=Order)

