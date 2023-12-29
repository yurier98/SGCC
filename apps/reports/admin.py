from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.reports.models import ReportRequest, ReportDefinition


# Register your models here.

@admin.register(ReportRequest)
class ReportRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('report_definition', 'is_test_data', 'created_on',)
    list_filter = ['is_test_data', 'created_on', ]


@admin.register(ReportDefinition)
class ReportDefinitionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('report_type', 'created_at', 'last_modified_at',)
    list_filter = ['last_modified_at', 'created_at', ]
