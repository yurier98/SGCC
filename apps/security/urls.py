from django.urls import path
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

]
