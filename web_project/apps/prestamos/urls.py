from django.urls import path
from django.views.generic import TemplateView

from ..prestamos import views

app_name = "prestamos"

urlpatterns = [
    # path('', TemplateView.as_view(template_name="prestamos/prestamos_list.html"), name='prestamos'),

    # path('', views.index, name='home'),
    #path('', views.index, name='home'),
    path('', views.PrestamosListView.as_view(), name='prestamos'),
    path('create', TemplateView.as_view(template_name="prestamos/prestamos_create.html"), name='create'),
]
