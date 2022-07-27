from django.urls import path
from django.views.generic import TemplateView

from ..reports import views
#from apps.reports.views import ReportLoanView



urlpatterns = [
    path('loan/', views.ReportLoanView.as_view(), name='report_loan'),
    path('inventory/', views.ReportInventoryView.as_view(), name='report_inventory'),
    #path('loan/', TemplateView.as_view(template_name="reports/reports_loan.html"), name='reports'),

    # path('', views.ProductListView.as_view(), name="inventory"),
    # # path('', views.ProductListView.as_view(), name=views.ProductListView.list_view_name),
    # path('create/', views.Create.as_view(), name='create'),
    # path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
    # path('edit/<int:pk>', views.Update.as_view(), name='update'),
    # path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
]
