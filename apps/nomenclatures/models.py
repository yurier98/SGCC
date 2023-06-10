from django.db import models
from django.forms import model_to_dict


# Create your models here.

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



class Manifestation(models.Model):
    """Manifestación model."""
    name = models.CharField("nombre", max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Manifestación"
        verbose_name_plural = "Manifestaciones"

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

