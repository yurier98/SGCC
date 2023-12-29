from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.utils import timezone
from apps.accounts.models import UserProfile
from apps.notification.models import SystemNotification
from apps.notification.views import NotificationListView


class NotificationListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword')
        self.notification = SystemNotification.objects.create(user=self.user, message='Test notification')

    def test_notification_list_view(self):
        request = self.factory.get('/notifications/')
        request.user = self.user

        response = NotificationListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notifications.html')
        self.assertContains(response, 'Test notification')
        self.assertTrue(response.context_data['all_notifications'].exists())
