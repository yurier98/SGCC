from django.urls import path

from . import views
from django.urls import path

from django.contrib.auth.views import LogoutView





urlpatterns = [

    # path('', views.RolListView.as_view(), name='rol_list'),
    # path('add/', views.RolCreateView.as_view(), name='rol_create'),
    # path('update/<int:pk>/', views.RolUpdateView.as_view(), name='rol_update'),
    # path('desactive/<int:pk>/', views.RolDesactiveView.as_view(), name='rol_delete'),
   # path('json/', views.json, name='json'),

    path('groups', views.GroupListView.as_view(), name='groups_list'),
    # path('add/', views.RolCreateView.as_view(), name='groups_create'),
    # path('update/<int:pk>/', views.RolUpdateView.as_view(), name='groups_update'),
    # path('desactive/<int:pk>/', views.RolDesactiveView.as_view(), name='groups_delete'),

]
