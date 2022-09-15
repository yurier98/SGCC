import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.forms import model_to_dict
from django.urls import reverse

# built-in signals
from django.db.models.signals import post_save

# signals
# from apps.order.models import Order
from apps.notification.signals import notificar

# Create your models here.
from apps.accounts.models import UserProfile
from apps.inventory.models import Product
from apps.order.models import Order


class Loan(models.Model):
    """Préstamo model."""

    ESTADO = (
        ('PE', 'Pendiente a autorización'),
        ('PR', 'Prestado'),
        ('EN', 'Entregado'),
    )
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # start_date = models.DateField("Fecha de inicio")
    # end_date = models.DateField("Fecha de devolución")
    # description = models.TextField("Descripción", help_text='Describa para que va a ser utilizado el medio prestado',
    #                                null=True, blank=True)
    # manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField("Estado", max_length=2, choices=ESTADO, default='PR')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        """Return title and username."""
        return 'Préstamo de {}'.format(self.order)

    # def toJSON(self):
    #     item = model_to_dict(self)
    #     item['number'] = self.get_number()
    #     item['start_date'] = self.start_date.strftime('%Y-%m-%d')
    #     item['end_date'] = self.end_date.strftime('%Y-%m-%d')
    #     item['created'] = self.created.strftime('%Y-%m-%d')
    #     item['user'] = self.user.toJSON()
    #     item['manifestation'] = self.manifestation.toJSON()
    #     item['loanproduct'] = [i.toJSON() for i in self.loanproduct_set.all()]
    #     return item

    def toJSON(self):
        item = model_to_dict(self)

        item['order'] = self.order.toJSON()
        # item['loanproduct'] = [i.toJSON() for i in self.orderproduct_set.all()]
        return item

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        # ordering = ["-created"]
        permissions = (
            ("report_loan", "Puede reportar Préstamos"),
        )


def notify_post(sender, instance, created, **kwargs):
    notificar.send(instance.user, destiny=instance.user, verb='Se ha creado un préstamo a su usuario exitosamente.',
                   level='success')


post_save.connect(notify_post, sender=Loan)
