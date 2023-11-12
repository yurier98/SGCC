""" Audit model admin """

# Django
from django.contrib import admin

# Models
from .models import Rule, Trace


@admin.register(Trace)
class TraceAdmin(admin.ModelAdmin):
    list_display = ("content_object", "action", "user", "ip", "os", "date")
    list_filter = ("action", "date")

    def get_date(self, obj):
        return obj.date


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    fields = ("content_type", "check_create", "check_edit", "check_delete", "is_active")
    list_display = (
        "is_active",
        "content_type",
        "check_create",
        "check_edit",
        "check_delete",
        "created_user",
        "modified_user",
    )
