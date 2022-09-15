from django.urls import path
from django.views.generic import TemplateView

from . import views
from ..inventory.views import CategoryListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView
from ..accounts.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView
from ..security.views import GroupListView, json, PermissionListView, GroupCreateView, GroupDeleteView, GroupUpdateView

# from ..order.views import ManifestationListView, ManifestationCreateView, ManifestationUpdateView, \
#     ManifestationDeleteView

# app_name = "admin"


urlpatterns = [
    # path('', TemplateView.as_view(template_name="admin/admin.html"), name='admin'),
    path('', views.HomePage.as_view(), name='home'),

    path('json/', json, name='json'),

    #################  Usuarios   #####################################
    path('user', UserListView.as_view(), name='user_list'),
    path('user/add', UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    # path('', UserListView.as_view(), name='user_list'),
    # path('add/', UserCreateView.as_view(), name='user_create'),
    # path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    # path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    #################  Manifestation   #####################################
    path('manifestation', views.ManifestationListView.as_view(), name='manifestation_list'),
    path('manifestation/add', views.ManifestationCreateView.as_view(), name='manifestation_create'),
    path('manifestation/update/<int:pk>/', views.ManifestationUpdateView.as_view(), name='manifestation_update'),
    path('manifestation/delete/<int:pk>/', views.ManifestationDeleteView.as_view(), name='manifestation_delete'),

    #################  Category   #####################################
    path('category', CategoryListView.as_view(), name='category_list'),
    path('category/add', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='manifestation_delete'),

    #################  Roles   #####################################
    path('rols', GroupListView.as_view(), name='group_list'),
    path('rols/add', GroupCreateView.as_view(), name='group_create'),
    path('rols/update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('rols/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),

    path('permission', PermissionListView.as_view(), name='permission_list'),

]
