from django.urls import path
from django.contrib.auth.decorators import permission_required
from django.views.generic import TemplateView
from ..order import views

urlpatterns = [

    # path('', views.OrderListView.as_view(), name='order_list'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('all', views.OrderListAllView.as_view(), name='order_all_list'),
    path('add', views.OrderCreateView.as_view(), name='order_create'),

    path('update/<uuid:pk>/', views.OrderUpdateView.as_view(), name='order_update'),
    path('all/update/<uuid:pk>/', views.OrderUpdatePermissionView.as_view(), name='order_update_permission'),

    path('detail/<uuid:pk>/', views.OrderDetailView.as_view(), name='order_detail'),

    path('delete/<uuid:pk>/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('invoice/pdf/<uuid:pk>/', views.OrderPdfView.as_view(), name='order_invoice_pdf'),
    # path('detail/approve/<int:pk>/', permission_required('order.approve_order')(views.ApproveView.as_view()),
    #      name='order_approve'),
    path('detail/approve/<uuid:pk>/', views.ApproveView.as_view(), name='order_approve'),
    path('detail/deny/<uuid:pk>/', views.ApproveView.as_view(), name='order_deny'),
]
