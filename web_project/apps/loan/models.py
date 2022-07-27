from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.forms import model_to_dict
from django.urls import reverse

# Create your models here.
from ..accounts.models import UserProfile
from ..inventory.models import Product


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
        ('PR', 'Prestado'),
        ('PE', 'Pendiente'),
        ('EN', 'Entregado'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_date = models.DateField("Fecha de inicio")
    end_date = models.DateField("Fecha de devolución")
    description = models.TextField("Descripción", help_text='Describa para que va a ser utilizado el medio prestado')
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    state = models.CharField("Estado", max_length=2, choices=ESTADO, default='PR')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and username."""
        return 'Préstamo a {}'.format(self.user.username)

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
