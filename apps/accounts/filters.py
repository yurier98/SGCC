import datetime
from django_filters import rest_framework as filters
from django import forms
from .models import Trace



def your_filter_date_update(queryset, value):
    today = datetime.date.today()

    if value == 'esta_semana':
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        print("Start of week:", start_of_week)
        print("End of week:", end_of_week)
        return queryset.filter(date__range=(start_of_week, end_of_week))

    if value == 'este_mes':
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
        print("Start of month:", start_of_month)
        print("End of month:", end_of_month)
        return queryset.filter(date__range=(start_of_month, end_of_month))

    if value == 'last_3_months':
        three_months_ago = today - datetime.timedelta(days=3 * 30)
        print("Three months ago:", three_months_ago)
        return queryset.filter(date__gte=three_months_ago)


class TraceFilter(filters.FilterSet):
    INTERVAL_CHOICES = [
        ('esta_semana', 'Esta Semana'),
        ('este_mes', 'Este Mes'),
        ('last_3_months', 'Últimos 3 Meses'),
    ]

    date = filters.ChoiceFilter(choices=INTERVAL_CHOICES,
                                       widget=forms.Select(attrs={'class': 'form-select w-auto'}),
                                       empty_label="Todos", # Aquí definimos el texto para la opción "Todos"
                                       method=lambda queryset, name, value: your_filter_date_update(queryset, value)
                                       )

    class Meta:
        model = Trace
        fields = ['action', 'date',]


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

