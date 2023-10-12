from django.contrib import admin

# Register your models here.
from apps.notification.models import  SystemNotification, EmailNotification


class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ('user','level', 'message', 'read')
    list_filter = ('level', 'read', 'is_delete')


class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('email_to', 'subject')
    # list_filter = ('created_at')


admin.site.register(SystemNotification, SystemNotificationAdmin)
admin.site.register(EmailNotification, EmailNotificationAdmin)



# admin.site.register(Notification, AbstractNotifyAdmin)
