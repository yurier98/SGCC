from django.contrib.auth.models import Group
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from swapper import load_model

from apps.accounts.models import UserProfile  # ver si mantengo esta
from apps.notification.signals import notificar


class BaseNotification(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class NotificationQueryset(models.QuerySet):

    def is_read(self):  # read  leido
        """
            Retornamos las notificaciones que hayan sido leidas
        """
        return self.filter(read=True)

    def unread(self):  # unread  no_leido
        """
            Retornamos solo los items que no hayan sido leidos        """
        return self.filter(read=False)

    def mark_all_as_read(self, user=None):  # mark_all_as_read   marcar_todo_as_leido
        """
            Marcar todas las notify como leidas
        """
        qs = self.read(False)
        if user:
            qs = qs.filter(user=user)
        return qs.update(read=True)

    def mark_all_as_unread(self, user=None):  # mark_all_as_unread   marcar_todo_as_no_leido
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
    email_to = models.EmailField('Enviar a')
    subject = models.CharField('Asunto', max_length=255)
    body = models.TextField('Descripción')

    def __str__(self):
        return f"Email notification '{self.subject}' sent to {self.email_to}"


class SystemNotification(BaseNotification):
    class Levels(models.TextChoices):
        SUCCESS = 'success', 'success',
        INFO = 'info', 'info',
        WRONG = 'wrong', 'wrong'
        ERROR = 'error', 'error'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', db_index=True)
    level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.INFO)
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
    # user= kwargs.pop('sender')
    created_at = kwargs.pop('created_at', timezone.now())

    Notify = load_model('notification', 'SystemNotification')
    levels = kwargs.pop('level', Notify.Levels.INFO)

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
