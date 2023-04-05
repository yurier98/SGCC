from django.db import models

# Create your models here.
from django.forms import model_to_dict
from apps.notification.utils.models import AbstractNotificacion

from apps.accounts.models import UserProfile




class Notification(AbstractNotificacion):

	class Meta(AbstractNotificacion.Meta):
		abstract = False
