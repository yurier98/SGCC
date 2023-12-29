import django_filters
from django_filters import filters
from .models import SystemNotification


class TimeFilter(django_filters.FilterSet):
    start_date = filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = SystemNotification
        fields = ['start_date', 'end_date']





