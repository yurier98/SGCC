from django.db import models
from django.forms import model_to_dict


# Create your models here.


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
