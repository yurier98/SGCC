from django.test import TestCase
from django.urls import reverse

from apps.loan.models import Loan
from apps.accounts.models import UserProfile


# Create your tests here.


class OrderTest(TestCase):

    def setUp(self) -> None:
        self.usuario = UserProfile.objects.create_user(username='usertest', password='passtest')
        self.client.login(username='usertest', password='passtest')

    def test_view(self):
        self.assertTrue(self.client.login(username='usertest', password='passtest'))
        res = self.client.get(reverse('order_list'))
        self.assertEqual(res.status_code, 200)
