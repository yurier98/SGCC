from django.urls import path
from django_filters.views import FilterView

from .filters import ProductFilter
from ..inventory import views

# app_name = "inventory"

urlpatterns = [
    path('', views.ProductListView.as_view(), name="inventory_list"),
    path('search/', views.ProductFilterView.as_view(), name="search"),
    # path('', views.ProductListView.as_view(), name=views.ProductListView.list_view_name),


    path('add', views.ProductCreateView.as_view(), name='product_create'),
    path('detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),




    # path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
    path('edit/<int:pk>', views.Update.as_view(), name='update'),
    # path('delete/<int:pk>', views.Delete.as_view(), name='product_delete'),

    #
    # path('search/$', FilterView.as_view(filterset_class=ProductFilter, template_name="inventory/inventory_list.html"),
    #      name='search'),
]
