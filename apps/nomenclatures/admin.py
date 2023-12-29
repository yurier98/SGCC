from django.contrib import admin

from apps.nomenclatures.models import Manifestation
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(Manifestation)
class ManifestationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('is_active', 'name', 'created_date', 'modified_date')
    list_filter = ['is_active', 'created_date', 'modified_date']
    # list_editable = ['is_active']
    # list_display_links = ['name']
    list_editable = ['is_active', 'name']
    list_display_links = None
