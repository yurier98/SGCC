from django.test import TestCase
from django.urls import reverse

from apps.loan.models import Loan
from apps.accounts.models import UserProfile


# Create your tests here.


class LoanTest(TestCase):

    def setUp(self) -> None:
        self.usuario = UserProfile.objects.create_user(username='usertest', password='passtest', )
        # self.mani = Manifestation.objects.create(name='ManifPrueba')
        self.auth = self.client.login(username='usertest', password='passtest')
        # self.loan = Loan.objects.create(user=self.usuario,
        #                                 start_date='2022-08-01',
        #                                 end_date='2022-08-02',
        #                                 description='',
        #                                 manifestation=self.mani,
        #                                 state='PR',
        #                                 )

    def test_view_loan(self):
        self.assertTrue(self.auth)

        # res = self.client.get(reverse('loan_list'))
        # self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('loan_create'))
        # ERROR 302 q no tiene permisos
        self.assertEqual(res.status_code, 200)

        # Buscar como pasarle un id a una url
        # res = self.client.get(reverse('sale_invoice_pdf', self.loan.id))
        # self.assertEqual(res.status_code, 200)

    def test_create_loan(self):
        self.assertTrue(self.client.login(username='usertest', password='passtest'))
        self.assertEqual(Loan.objects.count(), 0)
        data = {
            "user": self.usuario.id,
            "start_date": "20/02/2017",
            "end_date": "20/02/2017",
            "description": "PR",
            "manifestation": self.mani.id,
            "state": "PR",

        }
        # data['user'] = self.usuario.id
        # data['start_date'] = '25/08/2022'
        # data['end_date'] = '25/08/2022'
        # data['description'] = 'prueba'
        # data['manifestation'] = self.mani.id
        # data['state'] = 'PR'
        res = self.client.post(reverse('loan_create'), data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Loan.objects.count(), 0)

        # self.assertEqual(Loan.objects.get(denominacion='arquitecto').denominacion, "arquitecto")
        # self.assertEqual(Loan.objects.get(denominacion='arquitecto').descripcion, "arquitectoA")
        # self.assertEqual(Loan.objects.get(denominacion='arquitecto').publico, True)
        # self.assertEqual(Loan.objects.get(denominacion='arquitecto').activo, True)


# class ManifestationTest(TestCase):
#
#     def setUp(self) -> None:
#         self.usuario = UserProfile.objects.create_user(username='usertest', password='passtest', )
#         self.custom_auth = self.client.login(username='usertest', password='passtest')
#
#     def test_view_manifestation(self):
#         self.assertTrue(self.custom_auth)
#
#         # res = self.client.get(reverse('loan_list'))
#         # self.assertEqual(res.status_code, 200)
#
#         # res = self.client.get(reverse('loan_create'))
#         # ERROR 302 q no tiene permisos
#         # self.assertEqual(res.status_code, 302)
#
#         # Buscar como pasarle un id a una url
#         # res = self.client.get(reverse('sale_invoice_pdf', self.loan.id))
#         # self.assertEqual(res.status_code, 200)
#
#     def test_create_manifestation(self):
#         self.assertTrue(self.client.login(username='usertest', password='passtest'))
#         self.assertEqual(Manifestation.objects.count(), 0)
#         data = {
#             'name': 'Nombre de Prueba',
#         }
#         res = self.client.post(reverse('manifestation_create'), data)
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(Manifestation.objects.count(), 1)
#
#         mani = Manifestation.objects.all()[0]
#         self.assertEqual(mani.name, data['name'])
