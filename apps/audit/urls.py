from django.urls import path

# from apps.traces.views import TracesListView, TracesDeleteView, TracesDetailsView
# from apps.traces.views import TracesDeleteView
# from apps.traces.views import TracesDetailsView
from .views import TracesListView, RuleListView
from . import views

urlpatterns = [
    path('traces/', TracesListView.as_view(), name='traces_list'),
    path('rules/', RuleListView.as_view(), name='rule_list'),


    path('create_rule/', views.createregla, name='rule_create'),

    path('delete_trace/<int:pk>/', views.eliminartraza, name='traces_delete'),
    path('delete_rule/<int:pk>/', views.eliminarregla, name='rule_delete'),

    path('view_traza/<int:pk>/', views.viewtraza, name='view_traza'),

    path('list_traces/filter/', TracesListView.as_view(), name='traces_list_filter'),

    # path('list_rule/modify_rule', RuleCreateView.as_view(), name='rule_modify'),
    # path('delete_trace/<int:pk>/', TracesDeleteView.as_view(), name='traces_delete'),
    # path('delete_rule/<int:pk>/', TracesDeleteView.as_view(), name='rule_delete'),
    # path('details_traces/<int:pk>/', TracesDetailsView.as_view(), name='traces_details'),

    path('validate/', views.validate_rule_form, name='validate_rule_form'),
]
