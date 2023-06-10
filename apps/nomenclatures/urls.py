from django.urls import path
from . import views

# app_name = "admin"


urlpatterns = [

    #################  Manifestation   #####################################
    path('manifestations', views.ManifestationListView.as_view(), name='manifestation_list'),
    path('manifestation/add', views.ManifestationCreateView.as_view(), name='manifestation_create'),
    path('manifestation/update/<int:pk>/', views.ManifestationUpdateView.as_view(), name='manifestation_update'),
    path('manifestation/delete/<int:pk>/', views.ManifestationDeleteView.as_view(), name='manifestation_delete'),

    #################  Category   #####################################
    path('categorys', views.CategoryListView.as_view(), name='category_list'),
    path('category/add', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='manifestation_delete'),

]
