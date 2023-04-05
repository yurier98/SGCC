from django import forms
from .models import Order
import django_filters
from django_filters import filters


class OrderFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['description', 'manifestation', 'state']
