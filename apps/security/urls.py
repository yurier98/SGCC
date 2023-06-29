from django.urls import path
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.urls import path

from django.contrib.auth.views import LogoutView

urlpatterns = [

    # path('json/', views.json, name='json'),
    path('groups', views.GroupListView.as_view(), name='groups_list'),

    #################  Roles   #####################################
    path('rols', views.GroupListView.as_view(), name='group_list'),
    path('rols/add', views.GroupCreateView.as_view(), name='group_create'),
    path('rols/update/<int:pk>/', views.GroupUpdateView.as_view(), name='group_update'),
    path('rols/delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),

    #################  Permission   #####################################
    path('permission', views.PermissionListView.as_view(), name='permission_list'),
    # path('permission/add', views.PermissionCreateView.as_view(), name='permission_create'),
    # path('permission/update/<int:pk>/', views.PermissionUpdateView.as_view(), name='permission_update'),
    # path('permission/delete/<int:pk>/', views.PermissionDeleteView.as_view(), name='permission_delete'),
]
