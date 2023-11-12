import uuid
from datetime import datetime, timedelta
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
    # STATE = (
    #     ('Pendiente', 'Pendiente a autorización'),
    #     ('Prestado', 'Prestado'),
    #     ('Entregado', 'Entregado'),
    #     ('Atrasado', 'Atrasado'),
    # )

    class State(models.TextChoices):
        PENDIENTE = 'P', 'Pendiente a autorización'
        PRESTADO = 'PR', 'Prestado'
        ATRASADO = 'A', 'Atrasado'
        ENTREGADO = 'E', 'Entregado'


    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField("Estado", max_length=2, choices=State.choices, default=State.PENDIENTE)
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

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ["-order__created"]
        permissions = (
            ("report_loan", "Puede reportar Préstamos"),
        )

    def toJSON(self):
        item = model_to_dict(self)
        item['order'] = self.order.toJSON()
        # item['loanproduct'] = [i.toJSON() for i in self.orderproduct_set.all()]
        return item

    @classmethod
    def stats(self):
        # Obtener el total de préstamos
        total_orders = Loan.objects.all().count()
        # Obtener la fecha actual
        today = datetime.now().date()
        # Calcular la fecha hace 30 días
        last_month = today - timedelta(days=30)
        # Obtener el total de préstamos de los últimos 30 días
        last_month_loans = Loan.objects.filter(order__created__gte=last_month).count()
        # Calcular el porcentaje de aumento
        if last_month_loans > 0:
            increase = (total_orders - last_month_loans) / last_month_loans * 100
            increase = round(increase, 2)  # Redondear a dos lugares decimales
        else:
            increase = 0
        # Crear un diccionario con los valores estadísticos
        stats = {
            'total_loans': total_orders,
            'total_loans_slope': Loan.objects.filter(state=Loan.State.PENDIENTE).count(),
            'total_loans_provided': Loan.objects.filter(state=Loan.State.PRESTADO).count(),
            'total_loans_late': Loan.objects.filter(state=Loan.State.ATRASADO).count(),
            'total_loans_committed': Loan.objects.filter(state=Loan.State.ENTREGADO).count(),
            'last_month_loans': last_month_loans,
            'increase': increase,
        }
        return stats


def notify_post(sender, instance, created, **kwargs):
    user = instance.order.user
    notificar.send(user, destiny=user, verb='Se ha creado un préstamo a su usuario exitosamente.',
                   level='success')


post_save.connect(notify_post, sender=Loan)
