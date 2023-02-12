# Create your views here.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django_filters.views import FilterView

from apps.loan.models import Loan
from apps.inventory.models import Product
from apps.reports.forms import ReportForm
from apps.inventory.filters import ProductFilter
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from apps.reports.report import report


class ReportLoanView(ValidatePermissionRequiredMixin, FormView):
    template_name = 'reports/reports_loan.html'
    form_class = ReportForm
    permission_required = 'loan.report_loan'

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
        context['list_url'] = reverse_lazy('reports:report_loan')
        return context


class ReportInventoryView(ValidatePermissionRequiredMixin, FilterView):
    template_name = 'reports/reports_inventory.html'
    filterset_class = ProductFilter
    permission_required = 'inventory.report_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:report_inventory')
        return context


def exportProductPDF(request):
    """Example of ExportPDF"""
    products = Product.objects.all()

    products_list = []
    for product in products:
        products_list.append({
            'name': product.name,
            'category': product.category.name,
            'state': product.state
        })

    # person = Person.objects.filter(id=1).first()
    data = {
        'products': products_list,
        # 'image': convert_to_64(person.image.url)
    }

    return report(request, 'products', data)