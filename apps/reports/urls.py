from django.urls import path
from django.views.generic import TemplateView

from .report import edit,run,save
from ..reports import views
#from apps.reports.views import ReportLoanView



urlpatterns = [

    path('edit/<str:report_type>/', edit, name='report_edit'),
    path('run/', run, name='report_run'),
    path('save/<str:report_type>/', save, name='report_save'),






    path('loan/', views.ReportLoanView.as_view(), name='report_loan'),
    path('inventory/', views.ReportInventoryView.as_view(), name='report_inventory'),

    path('products/', views.exportProductPDF, name='report_products'),
    path('loans/', views.exportProductPDF, name='report_loans'),
    path('orders/', views.exportProductPDF, name='report_orders'),
    # path('products/', views.exportProductPDF, name='report_products'),



    #path('loan/', TemplateView.as_view(template_name="reports/reports_loan.html"), name='reports'),


]
