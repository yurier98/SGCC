from django import forms
from .models import Loan
import django_filters
from django_filters import filters

# from .models import Loan, Order


class LoanFilter(django_filters.FilterSet):
    order_created_at = django_filters.DateFilter(field_name='order__created_at')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Loan
        fields = ['state', 'order_created_at']


# class LoanFilter(django_filters.FilterSet):
#     description = django_filters.CharFilter(lookup_expr='icontains')
#     class Meta:
#         model = Loan
#         fields = ['order', 'state']
