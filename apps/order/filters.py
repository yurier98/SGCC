from django import forms
from .models import Order
import django_filters
from django_filters import filters

from ..nomenclatures.models import Category


class OrderFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    # product__category = django_filters.CharFilter(
    #     field_name='products__product__category__name',
    #     # Ajusta el campo según la relación entre Order y Product y la relación entre Product y Category
    #     # lookup_expr='icontains',
    #     label='Categoría del producto',
    # )
    product__category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),  # Asegúrate de importar el modelo Category
        field_name='products__product__category',
        # Ajusta el campo según las relaciones entre Order, Product y Category
        label='Categoría del producto',
    )

    class Meta:
        model = Order
        fields = ['description', 'manifestation', 'state', 'product__category']
        # se necesita add un campo para filtar el tipo de producto


