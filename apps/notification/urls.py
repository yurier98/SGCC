from django.urls import path
from django_filters.views import FilterView
from django.views.generic import TemplateView

from .filters import TimeFilter
from ..notification import views

# app_name = 'notification'

urlpatterns = [
    # path('', Index.as_view(), name='notification'),
    # path('', TemplateView.as_view(template_name="notifications/notifications.html"), name='notifications_list'),
    path('', views.NotificationListView.as_view(), name='notifications_list'),
    path('detail/<int:pk>/', views.NotificationDetailView.as_view(), name='notifications_detail'),

    path('all', views.NotificationListViewFilter.as_view(), name='notifications_list_all'),
    path('search/', FilterView.as_view(filterset_class=TimeFilter, template_name="notifications/notifications.html"),
         name='search'),

]
