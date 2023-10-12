# from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from django.forms import model_to_dict
# from apps.notification.utils.models import AbstractNotificacion

# from apps.accounts.models import UserProfile
# class Notification(AbstractNotificacion):

#	class Meta(AbstractNotificacion.Meta):
# abstract = False

#### aqui empiezan los cambios

from django.db import models
from django.utils import timezone
from swapper import load_model
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from apps.notification.signals import notificar
from apps.accounts.models import UserProfile  # ver si mantengo esta


class BaseNotification(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)


    class Meta:
        abstract = True
        ordering = ['-created_at']


class NotificationQueryset(models.QuerySet):

    def leido(self):
        """
            Retornamos las notificaciones que hayan sido leidas en el actual Queryset
        """
        return self.filter(read=True)

    def no_leido(self):
        """
            Retornamos solo los items que no hayan sido leidos en el actual Queryset
        """
        return self.filter(read=False)

    def marcar_todo_as_leido(self, user=None):
        """
            Marcar todas las notify como leidas en el actual queryset
        """
        qs = self.read(False)
        if user:
            qs = qs.filter(user=user)
        return qs.update(read=True)

    def marcar_todo_as_no_leido(self, user=None):
        """
            Marcar todas las notificaciones como no leidas en el actual queryset
        """
        qs = self.read(True)
        if user:
            qs = qs.filter(user=user)
        return qs.update(read=False)

class AbstractNotificationManager(models.Manager):
    def get_queryset(self):
        return self.NotificationQueryset(self.Model, using=self._db)





class EmailNotification(BaseNotification):
    email_to = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f"Email notification '{self.subject}' sent to {self.email_to}"


class SystemNotification(BaseNotification):
    class Levels(models.TextChoices):
        success = 'success', 'success',
        info = 'info', 'info',
        wrong = 'wrong', 'wrong'
        error = 'error', 'error'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', db_index=True)
    level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.info)
    message = models.CharField(max_length=255, default="")
    read = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    objects = NotificationQueryset.as_manager()

    def __str__(self):
        return f"System notification: {self.message}"





def notify_signals(message, **kwargs):
    """
        Funcion de controlador para crear una instancia de notificacion
        tras una llamada de signal de accion
    """

    user = kwargs.pop('user')
    created_at = kwargs.pop('created_at', timezone.now())
    Notify = load_model('notification', 'SystemNotification')
    levels = kwargs.pop('level', Notify.Levels.info)

    if isinstance(user, Group):
        destinies = user.user_set.all()
    elif isinstance(user, (QuerySet, list)):
        destinies = user
    else:
        destinies = [user]


    new_notify = []
    for destiny in destinies:

        notification = Notify(
            user=user,
            message=str(message),
            created_at=created_at,
            level=levels

        )

        notification.save()
        new_notify.append(notification)

    return new_notify


notificar.connect(notify_signals, dispatch_uid='notification.models.SystemNotification')

