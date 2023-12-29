from django.urls import path
from .report import edit, run, save
from . import views


urlpatterns = [

    path('edit/<str:report_type>/', edit, name='report_edit'),
    path('run/', run, name='report_run'),
    path('save/<str:report_type>/', save, name='report_save'),


    path('', views.ReportsView.as_view(), name='reports'),
    path('delete/<int:pk>/', views.report_delete, name='report_delete'),



    path('products/', views.exportProductPDF, name='report_products'),
    path('loans/', views.exportProductPDF, name='report_loans'),
    path('orders/', views.exportProductPDF, name='report_orders'),

]
