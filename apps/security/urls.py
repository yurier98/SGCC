from django.urls import path
from . import views

urlpatterns = [

    #################  Roles   #####################################
    path('group', views.GroupListView.as_view(), name='group_list'),
    path('group/<int:pk>/delete/', views.delete_group, name='group_delete'),


    path('group/add', views.GroupCreateView.as_view(), name='group_create'),
    # path('rols/update/<int:pk>/', views.GroupUpdateView.as_view(), name='group_update'),
    # path('rols/delete/<int:pk>/', views.GroupDeleteView.as_view(), name='group_delete'),

    #################  Permission   #####################################
    path('permission', views.PermissionListView.as_view(), name='permission_list'),

    path('ip-blocked', views.BlockedIPListView.as_view(), name='blocked_ip_list'),
    # path('permission/add', views.PermissionCreateView.as_view(), name='permission_create'),
    # path('permission/update/<int:pk>/', views.PermissionUpdateView.as_view(), name='permission_update'),
    # path('permission/delete/<int:pk>/', views.PermissionDeleteView.as_view(), name='permission_delete'),
]
