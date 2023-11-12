from django.urls import path
from . import views

urlpatterns = [

    path('', views.LoanListView.as_view(), name='loan_list'),
    # path('', views.LoanListView.as_view(), name='loan_list'),
    path('add', views.LoanCreateView.as_view(), name='loan_create'),
    path('invoice/pdf/<uuid:pk>/', views.LoanPdfView.as_view(), name='loan_invoice_pdf'),
    path('detail/<uuid:pk>/', views.LoanDetailView.as_view(), name='loan_detail'),

    # path('delete/<int:pk>/', views.LoanDeleteView.as_view(), name='loan_delete'),
    path('update/<uuid:pk>/', views.LoanUpdateView.as_view(), name='loan_update'),

]
