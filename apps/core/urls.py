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
    path('', views.HomePage.as_view(), name='home'),

    path('json/', json, name='json'),

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



]
