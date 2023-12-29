from contextlib import nullcontext
from django.utils import timezone
from django.db import models
from django.db.models import ImageField
from django.forms import model_to_dict
from django.urls import reverse
from config.settings import base
from apps.nomenclatures.models import AbstractBaseNomenclature
from apps.utils import optimize_image


# Create your models here.


class ProductAttribute(models.Model):
    """Categoría de producto model."""
    atributo = models.CharField("Atributo", max_length=50, unique=True)
    valor = models.CharField("Valor", max_length=50, unique=True)

    class Meta:
        verbose_name = "Atributo"
        verbose_name_plural = "Atributos"
        # app_label = 'loan'

    def __str__(self):
        return self.atributo


class Category(AbstractBaseNomenclature):
    name = models.CharField("Categoría del producto", max_length=50, unique=True)

    # slug = models.SlugField(max_length=200, default='null', db_index=True, unique=True)

    class Meta:
        # ordering = 'name'
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de los productos'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop:product_list_by_category', args=[self.slug])
    def toJSON(self):
        item = model_to_dict(self)
        return item


class Product(models.Model):
    ESTADO = (
        ('D', 'Disponible'),
        ('P', 'Prestado'),
    )
    # id_producto = models.AutoField(primary_key=True)

    name = models.CharField("Nombre del producto", max_length=100)
    img = ImageField(verbose_name='Imagen del producto', upload_to='products/%Y/%m/%d', null=True, blank=True,
                     default='no_picture.jpg',
                     help_text="Se recomienda que las imágenes que seleccione tenga el formato PNG o JPG.")

    state = models.CharField("Estado", max_length=1, choices=ESTADO, default='D')
    stock = models.PositiveIntegerField('Cantidad de unidades')
    active = models.BooleanField('Está activo', default=True,
                                 help_text="Si no está marcado, le permitirá ocultar el producto sin eliminarlo.")
    available = models.BooleanField("Está disponible", default=True,
                                    help_text="Marcar si el producto está disponible en el sistema.")

    category = models.ForeignKey(Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True, )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def get_absolute_url(self):
        return reverse('inventory:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name}'

    @property
    def recently_created(self) -> bool:
        return (timezone.now() - self.created_at) <= timezone.timedelta(days=5)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        category = self.category
        if category:
            item['category'] = category.toJSON()
        else:
            item['category'] = 'N/A'
        item['img'] = self.get_image()
        item['created'] = self.created_at.strftime('%Y-%m-%d')
        return item

    def get_image(self):
        if self.img:
            return f'{base.MEDIA_URL}{self.img}'
        return f'{base.MEDIA_URL}no_picture.jpg'

    def save(self, *args, **kwargs):
        # Llama al método save() del modelo para guardar la imagen original
        super(Product, self).save(*args, **kwargs)

        # Optimizamos la imagen antes de guardarla
        if self.img:
            # Llama a la función optimize_image para optimizar la imagen
            optimize_image(self.img.path)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

        permissions = (
            # ("producto", "Puede hacer TODAS las operaciones de productos"),
            # ("producto_index", "Puede ver el index de productos"),
            # ("producto_add", "Puede agregar producto"),
            # ("producto_edit", "Puede actualizar productos"),
            # ("producto_delete", "Puede eliminar productos"),
            ("report_product", "Puede reportar productos"),
            # ("producto_state", "Puede inactivar y reactivar productos"),
            # Pa agregar más permissions solo vuelva a hacer >python manage.py syncdb y no tiene que borrar la db
            # ("producto_list", "xPuede listar productos"),
            # ("producto_json", "xPuede listar productos en formato JSON"),
            # ("producto_edit_precio", "Puede actualizar precio venta de productos"),
        )
