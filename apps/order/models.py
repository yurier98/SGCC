import uuid
from django.db import models
from django.forms import model_to_dict

# Create your models here.
from apps.accounts.models import UserProfile
from apps.inventory.models import Product
from apps.core.models import Manifestation



class Order(models.Model):
    """Pedido model. """

    STATE = (
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField("Fecha de inicio")
    end_date = models.DateField("Fecha de devolución")
    description = models.TextField("Descripción", help_text='Describa para que va a ser utilizado el medio prestado',
                                   null=True, blank=True)
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    state = models.CharField("Estado", max_length=11, choices=STATE, default='Pendiente')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        """Return title and username."""
        return 'Pedido de {}'.format(self.user.username)

    def toJSON(self):
        item = model_to_dict(self)
        # item['id'] = self.id
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['created'] = self.created.strftime('%Y-%m-%d')
        item['user'] = self.user.toJSON()
        item['manifestation'] = self.manifestation.toJSON()
        item['orderproduct'] = [i.toJSON() for i in self.orderproduct_set.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.orderproduct_set.all():
            detail.product.stock += detail.cant
            detail.product.save()
        super(Order, self).delete()

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created"]
        permissions = (
            ("approve_order", "Aprobar Pedido"),
            ("view_all_order", "Ver todos los pedidos"),
        )


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='Listados_de_items', on_delete=models.CASCADE)
    cant = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['order'])
        item['product'] = self.product.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle del pedido'
        verbose_name_plural = 'Detalle de los pedidos'
        default_permissions = ()
        ordering = ['id']

# def notify_post(sender, instance, created, **kwargs):
#     notificar.send(instance.user, destiny=instance.user, verb='Se ha creado un pedido a su usuario exitosamente.',
#                    level='success')
#
#
# post_save.connect(notify_post, sender=Order)
