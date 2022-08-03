from django.db import models

# Create your models here.
from django.forms import model_to_dict
from apps.notification.utils.models import AbstractNotificacion

from apps.accounts.models import UserProfile




class Notification(AbstractNotificacion):

	class Meta(AbstractNotificacion.Meta):
		abstract = False


#
# class Notification(models.Model):
#     """Notificacion model."""
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100, null=True)
#     msg = models.TextField("Mensaje")
#     is_seen = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return title and username."""
#         return 'Notificación a {} el {}'.format(self.user.username, self.created)
#
#     def toJSON(self):
#         item = model_to_dict(self)
#         item['user'] = self.user.toJSON()
#         item['created'] = self.created.strftime('%Y-%m-%d')
#         return item
#
#     class Meta:
#         verbose_name = "Notificación"
#         verbose_name_plural = "Notificaciones"
#         ordering = ['-created']
