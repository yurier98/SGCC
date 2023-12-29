from django_filters import rest_framework as filters
from .models import UserProfile


class UserFilter(filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = ['groups', 'is_active',]



