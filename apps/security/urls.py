from django.urls import path
<<<<<<< HEAD

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
=======
from . import views

urlpatterns = [

    # path('json/', views.json, name='json'),

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
>>>>>>> origin/main

]
