from django.urls import path
from django_filters.views import FilterView

from .filters import ProductFilter
from ..inventory import views

# app_name = "inventory"

urlpatterns = [
    path('', views.ProductListView.as_view(), name="inventory_list"),
    path('add', views.ProductCreateView.as_view(), name='product_create'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]
