from uuid import uuid4
from datetime import datetime, timedelta
from django.db import models, connection
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.
from apps.accounts.models import UserProfile
from apps.inventory.models import Product
from apps.nomenclatures.models import Manifestation

User = get_user_model()
last_order_number = 0


def get_order_number():
    global last_order_number
    if 'sqlite' in connection.vendor:
        last_order_number += 1
        return last_order_number
    elif 'postgresql' in connection.vendor:
        # Utiliza la secuencia de PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT nextval('order_order_number_seq')")
            result = cursor.fetchone()
            return result[0]
    else:
        # Otros sistemas de base de datos no son compatibles
        raise NotImplementedError("Este sistema de base de datos no es compatible con la función get_order_number()")


class Order(models.Model):
    """Pedido model. """

    class State(models.TextChoices):
        PENDIENTE = 'P', 'Pendiente'
        APROBADO = 'A', 'Aprobado'
        RECHAZADO = 'R', 'Rechazado'

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid4)
    # number = models.IntegerField(unique=True, default=get_order_number, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField("Fecha de inicio")
    end_date = models.DateField("Fecha de devolución")
    description = models.TextField("Descripción", help_text='Describa para que va a ser utilizado el medio prestado',
                                   null=True, blank=True)
    manifestation = models.ForeignKey(Manifestation, on_delete=models.CASCADE)
    state = models.CharField("Estado", max_length=1, choices=State.choices, default=State.PENDIENTE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, db_index=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        """Return title and username."""
        return 'Pedido de {}'.format(self.user.username)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]
        permissions = (
            ("approve_order", "Aprobar Pedido"),
            ("view_all_order", "Ver todos los pedidos"),
        )

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date cannot be before start date")

    def toJSON(self):
        item = model_to_dict(self)
        # item['id'] = self.id
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['created'] = self.created_at.strftime('%Y-%m-%d')
        item['user'] = self.user.toJSON()
        item['manifestation'] = self.manifestation.toJSON()
        item['orderproduct'] = [i.toJSON() for i in self.products.all()]
        return item

    def delete(self, using=None, keep_parents=False):
        for detail in self.products.all():
            detail.product.stock += detail.cant
            detail.product.save()
        super(Order, self).delete()

    @classmethod
    def stats(self):
        # Obtener la fecha actual
        today = datetime.now().date()
        # Calcular la fecha hace 30 días
        last_month = today - timedelta(days=30)
        # Obtener el total de pedidos de los últimos 30 días
        last_month_orders = Order.objects.filter(created_at__gte=last_month).count()
        # Obtener el total de pedidos
        total_orders = Order.objects.all().count()
        # Calcular el porcentaje de aumento
        if last_month_orders > 0:
            increase = (total_orders - last_month_orders) / last_month_orders * 100
            increase = round(increase, 2)  # Redondear a dos lugares decimales
        else:
            increase = 0
        # Crear un diccionario con los valores estadísticos
        stats = {
            'total_orders': total_orders,
            'total_orders_pending': Order.objects.filter(state=Order.State.PENDIENTE).count(),
            'total_orders_approve': Order.objects.filter(state=Order.State.APROBADO).count(),
            'total_orders_rejected': Order.objects.filter(state=Order.State.RECHAZADO).count(),
            'last_month_orders': last_month_orders,
            'increase': increase,
        }
        return stats

    @classmethod
    def total_orders(cls):
        return cls.objects.count()

    @classmethod
    def total_orders_pending(cls):
        return cls.objects.filter(state='Pendiente').count()

    @classmethod
    def total_orders_approve(cls):
        return cls.objects.filter(state='Aprobado').count()

    @classmethod
    def total_orders_rejected(cls):
        return cls.objects.filter(state='No Aprobado').count()

    def cantidad_prestamos(self):
        return Order.objects.count()

    def porcentaje_pendientes(self):
        total_prestamos = self.total_orders()
        prestamos_pendientes = self.total_orders_pending()
        return (prestamos_pendientes / total_prestamos) * 100


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
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
