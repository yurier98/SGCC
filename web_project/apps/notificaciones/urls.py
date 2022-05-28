from django.urls import path
from django.views.generic import TemplateView

from .views import Index

app_name = 'notificaciones'

urlpatterns = [
    #path('', Index.as_view(), name='notificaciones'),
    path('', TemplateView.as_view(template_name="notificaciones/notifications.html"), name='notificaciones'),
]
