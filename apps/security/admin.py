from django.contrib import admin
from .models import BlockedIP


# Register your models here.


class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'date_added', 'date_unblocked')
    search_fields = ('ip_address',)


admin.site.register(BlockedIP, BlockedIPAdmin)
