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


class Manifestation(models.Model):
    """Manifestación model."""
    name = models.CharField("nombre", max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Manifestación"
        verbose_name_plural = "Manifestaciones"
        app_label = 'loan'

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Loan(models.Model):
    """Préstamo model.

    """
    ESTADO = (
        ('PE', 'Pendiente a autorización'),
        ('PR', 'Prestado'),
        ('EN', 'Entregado'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField("Fecha de inicio")
    end_date = models.DateField("Fecha de devolución")
    description = models.TextField("Descripción", help_text='Describa para que va a ser utilizado el medio prestado',
                                   null=True, blank=True)
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    state = models.CharField("Estado", max_length=2, choices=ESTADO, default='PR')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username."""
        return 'Préstamo de {}'.format(self.user.username)

    def get_number(self):
        return f'{self.id:06d}'

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = self.get_number()
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['created'] = self.created.strftime('%Y-%m-%d')
        item['user'] = self.user.toJSON()
        item['manifestation'] = self.manifestation.toJSON()
        item['loanproduct'] = [i.toJSON() for i in self.loanproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.loanproduct_set.all():
            detail.product.stock += detail.cant
            detail.product.save()
        super(Loan, self).delete()

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ["-created"]
        permissions = (
            ("report_loan", "Puede reportar Préstamos"),
        )


class LoanProduct(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='Listados_de_productos', on_delete=models.CASCADE)
    cant = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['loan'])
        item['product'] = self.product.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle del préstamo'
        verbose_name_plural = 'Detalle de los préstamos'
        default_permissions = ()
        ordering = ['id']


def notify_post(sender, instance, created, **kwargs):
    notificar.send(instance.user, destiny=instance.user, verb='Se ha creado un préstamo a su usuario exitosamente.',
                   level='success')


post_save.connect(notify_post, sender=Loan)

# @receiver(post_save, sender=Order)
# def create_loan(sender, instance, **kwargs):
#     id_order = instance.order.id
#     user = instance.order.user_id
#     start_date = instance.order.start_date
#     end_date = instance.order.end_date
#     description = instance.order.description
#     manifestation = instance.order.manifestation_id
#     state = instance.order.state
#     print(state)
#
#     loan = Loan(user, start_date, end_date, description, manifestation)
#     loan.save()
#
#     if state.__eq__('Aprobado'):
#         loan = Loan(user, start_date, end_date, description, manifestation)
#         loan.save()
