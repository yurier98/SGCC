from django.contrib import admin

# Register your models here.
from ..notification.models import Notification
from apps.notification.utils.admin import AbstractNotifyAdmin


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_seen', 'created', ]
    list_filter = ['is_seen', 'created']
    autocomplete_fields = ['user']


# admin.site.register(Notification, NotificationAdmin)
admin.site.register(Notification, AbstractNotifyAdmin)
