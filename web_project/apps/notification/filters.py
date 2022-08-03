from django import forms
from .models import Notification
import django_filters
from django_filters import filters

# class NotificationFilter(django_filters.FilterSet):
#


class TimeFilter(django_filters.FilterSet):
    start_date = filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = Notification
        fields = ['start_date', 'end_date']





