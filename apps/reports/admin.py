from django.contrib import admin

from apps.reports.models import ReportRequest,ReportDefinition

# Register your models here.
admin.site.register(ReportRequest)
admin.site.register(ReportDefinition)
