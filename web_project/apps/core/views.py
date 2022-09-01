from datetime import date

from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, View, DetailView, TemplateView

#
# def homepage(request):
#     return render(request, "index.html")
#
from apps.inventory.models import Product
from apps.loan.models import Loan
from apps.order.models import Order


class HomePage(TemplateView):
    template_name = 'index.html'

    # cantProductos = Product.objects.all().count()
    # totalLoan = Loan.objects.all().count()
    # loanpendiente = Loan.objects.all().filter(state='PR').count()


    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        loanp = Loan.objects.all().filter(state='PR')
        cont = 0
        for i in loanp:
            date = i.end_date
            if date.today() > date:
                cont += 1
        context['title'] = 'Inicio'
        context['cantProductos'] = Product.objects.all().count()
        context['totalLoan'] = Loan.objects.all().count()
        context['loanpendiente'] = Loan.objects.all().filter(state='PR').count()
        context['orderPendiente'] = Order.objects.all().filter(state='Pendiente').count()
        context['loanFaltantes'] = cont
        return context
