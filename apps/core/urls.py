from django.urls import path
from . import views
from apps.security.views import GroupListView, json






urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('json/', json, name='json'),

    path('messages/', views.get_messages, name='get_messages'),

]
