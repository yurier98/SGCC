from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

# Create your models here.
from datetime import datetime, timedelta
from django.utils import timezone


class AbstractBaseNomenclature(models.Model):
    """Nomenclatures base model which every models inherit."""

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación"
    )
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name="última fecha de modificación"
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    class Meta:
        """Meta options."""
        abstract = True


class Manifestation(AbstractBaseNomenclature):
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
