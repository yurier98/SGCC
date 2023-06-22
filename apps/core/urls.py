from django.urls import path
from . import views
from ..security.views import json


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('json/', json, name='json'),

]
