from django.contrib import admin

# Register your models here.
from ..notification.models import Notification


class AbstractNotifyAdmin(admin.ModelAdmin):
    raw_id_fields = ('destiny',)
    list_dysplay = ('destiny', 'actor', 'verbo', 'read', 'publico')
    list_filter = ('level', 'read', 'destiny')

    def get_queryset(self, requets):
        qs = super(AbstractNotifyAdmin, self).get_queryset(requets)
        return qs.prefetch_related('actor')



# admin.site.register(Notification, NotificationAdmin)
admin.site.register(Notification, AbstractNotifyAdmin)
