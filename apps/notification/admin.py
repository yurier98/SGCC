from django.contrib import admin

# Register your models here.
from apps.notification.models import  SystemNotification, EmailNotification

@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ('user','level', 'message', 'read', 'is_delete')
    list_filter = ('level', 'read', 'is_delete')
    actions = ['mark_all_as_read', 'mark_all_as_undelete']
    def mark_all_as_read(self, request, queryset):
        queryset.update(read=False)

    def mark_all_as_undelete(self, request, queryset):
        queryset.update(is_delete=False)

    mark_all_as_read.short_description = "Marcar como no leído"
    mark_all_as_undelete.short_description = "Marcar como no eliminado"

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('email_to', 'subject')
    # list_filter = ('created_at')




