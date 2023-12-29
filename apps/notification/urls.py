from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notifications_list"),
    # path('email-notification/<uuid:pk>', views.SendEmailView.as_view(), name='notify_by_email'),
    path('email-notification/<uuid:pk>', views.SendEmailView2.as_view(), name='notify_by_email'),

]

htmx_urlpatterns = [
    path('delete-notification/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('mark-read-notification/', views.mark_all_as_read, name='notification_mark_all_as_read'),
]

urlpatterns += htmx_urlpatterns
