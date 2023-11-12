import datetime
from django import forms
from .models import Loan
import django_filters
# from django_filters import filters
from django_filters import rest_framework as filters

# from .models import Loan, Order


def your_filter_date_update(queryset, value):
    today = datetime.date.today()

    if value == 'esta_semana':
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        print("Start of week:", start_of_week)
        print("End of week:", end_of_week)
        return queryset.filter(order__updated__range=(start_of_week, end_of_week))

    if value == 'este_mes':
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
        print("Start of month:", start_of_month)
        print("End of month:", end_of_month)
        return queryset.filter(order__updated__range=(start_of_month, end_of_month))

    if value == 'ultimos_tres_meses':
        three_months_ago = today - datetime.timedelta(days=3 * 30)
        print("Three months ago:", three_months_ago)
        return queryset.filter(order__updated__gte=three_months_ago)


class LoanFilter(filters.FilterSet):
    description_contains = filters.CharFilter(field_name='order__description', lookup_expr='icontains',
                                              label='Descripción de la Order')

    # order_created_at = django_filters.DateFilter(field_name='order__created_at')
    # status = django_filters.CharFilter(field_name='status')


    STATUS_CHOICES = [
        ('', 'Todos'),  # Opción "Todos" sin valor de filtro
        ('P', 'Pendiente a autorización'),
        ('PR', 'Prestado'),
        ('E', 'Entregado'),
        ('A', 'Atrasado'),
    ]

    state = filters.CharFilter(
        field_name='state',
        widget=forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
        # widget=forms.Select(choices=Loan.State.choices, attrs={'class': 'form-control'}),
    )

    INTERVAL_CHOICES = [
        ('esta_semana', 'Esta Semana'),
        ('este_mes', 'Este Mes'),
        ('ultimos_tres_meses', 'Últimos 3 Meses'),
    ]
    # date_update = filters.ChoiceFilter(choices=INTERVAL_CHOICES,
    #                             widget=forms.Select(attrs={'class': 'form-select w-auto'}),
    #                             empty_label="Todos"  # Aquí definimos el texto para la opción "Todos"
    #                             )
    date_update = filters.ChoiceFilter(choices=INTERVAL_CHOICES,
                                       widget=forms.Select(attrs={'class': 'form-select w-auto'}),
                                       empty_label="Todos", # Aquí definimos el texto para la opción "Todos"
                                       method=lambda queryset, name, value: your_filter_date_update(queryset, value)
                                       )

    class Meta:
        model = Loan
        fields = ['state', 'date_update', 'description_contains']

    def filter_description_contains(self, queryset, name, value):
        return queryset.filter(order__description__icontains=value)

    def filter_date_update(self, queryset, name, value):
        today = datetime.date.today()
        print("Debug message: Inside filter_date_update")

        if value == 'esta_semana':
            start_of_week = today - datetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + datetime.timedelta(days=6)
            print("Start of week:", start_of_week)
            print("End of week:", end_of_week)
            return queryset.filter(order__updated__range=(start_of_week, end_of_week))

        if value == 'este_mes':
            start_of_month = today.replace(day=1)
            end_of_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
            return queryset.filter(order__updated__range=(start_of_month, end_of_month))

        if value == 'ultimos_tres_meses':
            three_months_ago = today - datetime.timedelta(days=3 * 30)
            return queryset.filter(order__updated__gte=three_months_ago)



# class LoanFilter(django_filters.FilterSet):
#     description = django_filters.CharFilter(lookup_expr='icontains')
#     class Meta:
#         model = Loan
#         fields = ['order', 'state']
