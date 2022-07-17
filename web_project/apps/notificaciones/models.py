from django.db import models


# Create your models here.
class Notificacion(models.Model):
    """Manifestacion model."""
    user = models.CharField(max_length=100, unique=True)
    msg = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.created
