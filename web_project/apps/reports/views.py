from django.shortcuts import render
import json
# Create your views here.
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.db.models import Q
from django.db import transaction
from apps.loan.models import Loan
from apps.inventory.models import Product, Category
from apps.reports.forms import ReportForm, ReportFilter


class ReportLoanView(FormView):
    template_name = 'reports/reports_loan.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                queryset = Loan.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(created__range=[start_date, end_date])
                    # queryset = queryset.filter(start_date=start_date)
                    # queryset = queryset.filter(end_date=end_date)
                    for q in queryset:
                        print(q)
                # lists=queryset

                for s in queryset:
                    # print(s)
                    # for i in s:
                    #     print(i.toJSON)
                    data.append(s.toJSON())

                    # data.append([
                    #     s.id,
                    #     # f'{s.user.first_nam + s.user.last_name}',
                    #     s.user.get_full_name(),
                    #     s.user.area,
                    #     s.user.phone,
                    #     s.user.phone,
                    #     s.user.phone,
                    #     # s.loanproduct_set.product.name,
                    #     # s.loanproduct_set,
                    #     # s.user.first_name,
                    #     # s.created.strftime('%Y-%m-%d'),
                    #
                    # ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Préstamos'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report_loan')
        return context


class ReportInventoryView(FormView):
    template_name = 'reports/reports_inventory.html'
    form_class = ReportFilter

    # model = Product

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            queryset = Product.objects.all()
            action = request.POST['action']
            if action == 'search':
                data = []

                """Dos via para devolver los datos """
                """si pongo esta debo quitar el comentario de la datatable en el js
                """
                # for i in queryset:
                #     item = i.toJSON()
                #     item['value'] = i.__str__()
                #     data.append(item)

                #     # data.append(i.toJSON())
                for i in queryset:
                    data.append([
                        i.id,
                        i.name,
                        i.category.name,
                        i.stock,
                        i.created.strftime('%Y-%m-%d'),
                    ])

            elif action == 'search_filter':
                data = []
                state = request.POST['state']
                category = request.POST['category']

                if len(state) and len(category):
                    queryset = queryset.filter(state=state, category=category)
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
                    # data.append(i.toJSON())

                # for s in queryset:
                #     data.append([
                #         s.id,
                #         s.name,
                #         s.category.name,
                #         s.stock,
                #         s.created.strftime('%Y-%m-%d'),
                #
                #     ])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('report_inventory')
        return context
