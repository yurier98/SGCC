from django import forms
from .models import Product
import django_filters
from django_filters import filters


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'category', 'state']
