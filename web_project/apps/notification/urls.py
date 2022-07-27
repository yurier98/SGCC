from django.urls import path
from django.views.generic import TemplateView

from .views import Index

app_name = 'notification'

urlpatterns = [
    #path('', Index.as_view(), name='notification'),
    path('', TemplateView.as_view(template_name="notificaciones/notifications.html"), name='notification'),
]
