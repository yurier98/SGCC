from django.contrib import admin

import csv
import datetime
from django.http import HttpResponse
# Register your models here.
from django.urls import reverse
from django.utils.html import format_html

from .models import Loan


# class LoanItemInline(admin.TabularInline):
#     model = LoanProduct
#     raw_id_fields = ['order']


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


def order_detail(instance):
    # return '<a href="{}">View</a>'.format(reverse('loan:admin_order_detail', args=[obj.id]))
    return format_html('<a class="button" href="{}">Ver</a>'.format(reverse('order_detail', args=[instance.order.pk])))


order_detail.allow_tags = True


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('order', 'state', order_detail)
    list_filter = ('state', 'order__updated')
    # list_editable = ('state',)
    # autocomplete_fields = ['user']
    # inlines = [LoanItemInline]
    actions = [export_to_csv]
