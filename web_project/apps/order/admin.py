from django.contrib import admin
import csv
import datetime
from django.http import HttpResponse
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderProduct


class OrderItemInline(admin.TabularInline):
    model = OrderProduct
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    # return '<a href="{}">View</a>'.format(reverse('loan:admin_order_detail', args=[obj.id]))
    return format_html('<a class="button" href="{}">Ver</a>'.format(reverse('order_update', args=[obj.id])))


order_detail.allow_tags = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date', 'manifestation', 'state',
                    order_detail]
    list_filter = ['manifestation', 'state', 'updated']
    autocomplete_fields = ['user']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


admin.site.register(Order, OrderAdmin)
