from contextlib import nullcontext

from django.db import models
from django.db.models import ImageField
from django.forms import model_to_dict
from django.urls import reverse

# Create your models here.
from config.settings import base




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


class Category(models.Model):
    name = models.CharField("Categoría del producto", max_length=50, unique=True)

    # slug = models.SlugField(max_length=200, default='null', db_index=True, unique=True)

    class Meta:
       # ordering = 'name'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

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
    category = models.ForeignKey(Category, verbose_name=("Categoria del producto"), on_delete=models.PROTECT)
    name = models.CharField("Nombre del producto", max_length=100)
    img = ImageField(upload_to='products', null=True, blank=True, default='no_picture.svg')

    state = models.CharField("Estado", max_length=1, choices=ESTADO, default='D')
    stock = models.PositiveIntegerField('Cantidad de unidades')
    active = models.BooleanField('Activo', default=True,
                                 help_text="Si no está marcado, le permitirá ocultar el producto sin eliminarlo.")
    available = models.BooleanField("Disponible", default=True,
                                    help_text="Marcar si el producto está disponible en el sistema.")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return reverse('inventory:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['category'] = self.category.toJSON()
        item['img'] = self.get_image()
        return item

    def get_image(self):
        if self.img:
            return f'{base.MEDIA_URL}{self.img}'
        return f'{base.STATIC_URL}/no_picture.svg'


    class Meta:
        ordering = ["-created"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
