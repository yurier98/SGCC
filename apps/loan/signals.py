# Django
# from .models import Loan, LoanProduct
# from apps.order.models import Order, OrderProduct
# from django.dispatch import Signal
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# def metodo(self, order, orderproduct_set):
#     loan = Loan()
#     loan.start_date = order.start_date
#     loan.end_date = order.end_date
#     loan.user_id = order.user_id
#     loan.description = order.description
#     loan.state = order.state
#     loan.manifestation_id = order.manifestation_id
#     loan.save()
#
#     loanproduct = LoanProduct()
#     loanproduct.loan_id = orderproduct_set.order_id
#     loanproduct.product_id = orderproduct_set.product_id
#     loanproduct.cant = orderproduct_set.cant
#     loanproduct.save()

#
# @receiver(post_save, sender=Order)
# def post_save_create_loan(sender, instance, created, **kwargs):
#     print(sender)
#     print(instance)
#     print(created)
#
#     if created:
#         Loan.objects.create(user=instance)

