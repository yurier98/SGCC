from django.urls import path
from django.views.generic import TemplateView

from ..loan import views

#app_name = "loan"




urlpatterns = [
    # path('', TemplateView.as_view(template_name="loan/list_loan.html"), name='loan'),
    # path('', views.index, name='home'),
    # path('', views.LoanListView.as_view(), name='loan'),
    # path('create', TemplateView.as_view(template_name="loan/create_loan.html"), name='create'),
    # path('create', views.Create.as_view(), name='create'),
    # path('search_product', views.Search_Producto.as_view(), name='search_product'),

    path('', views.LoanListView.as_view(), name='loan_list'),
    path('add', views.LoanCreateView.as_view(), name='loan_create'),
    path('delete/<int:pk>/', views.LoanDeleteView.as_view(), name='loan_delete'),
    path('update/<int:pk>/', views.LoanUpdateView.as_view(), name='loan_update'),

    path('invoice/pdf/<int:pk>/', views.LoanPdfView.as_view(), name='sale_invoice_pdf'),
]
