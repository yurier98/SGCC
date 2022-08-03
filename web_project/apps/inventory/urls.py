from django.urls import path
from django_filters.views import FilterView

from .filters import ProductFilter
from ..inventory import views

app_name = "inventory"

urlpatterns = [
    path('', views.ProductListView.as_view(), name="inventory"),
    path('search/$', views.ProductFilterView.as_view(), name="search"),
    # path('', views.ProductListView.as_view(), name=views.ProductListView.list_view_name),
    path('create/', views.Create.as_view(), name='create'),
    path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
    path('edit/<int:pk>', views.Update.as_view(), name='update'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),


    #
    # path('search/$', FilterView.as_view(filterset_class=ProductFilter, template_name="inventory/inventory_list.html"),
    #      name='search'),
]
