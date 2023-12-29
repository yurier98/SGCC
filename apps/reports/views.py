# Create your views here.
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django_filters.views import FilterView
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.shortcuts import redirect
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from apps.inventory.models import Product
from apps.inventory.filters import ProductFilter

from .forms import ReportForm
from .models import ReportDefinition
from .report import report
from apps.reports.utils import convert_to_64

MODULE_NAME = 'Reportes'


class ReportsView(ListView):
    model = ReportDefinition
    template_name = 'reports/reports.html'

    # permission_required = 'reports.reports_view'

    def post(self, request, *args, **kwargs):
        ReportDefinition_id = request.POST.get('id')

        if ReportDefinition_id:
            instance = ReportDefinition_id.objects.get(id=ReportDefinition_id)
            form = ReportForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Se ha modificado el nombre un reporte.')
            else:
                print(form.errors)
                messages.error(request, 'Formulario inválido.')
        else:
            form = ReportForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Se ha creado un reporte nuevo.')
            else:
                messages.error(request, 'Formulario inválido.')
        return redirect('reports')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Listado de plantillas'
        context['list_url'] = reverse_lazy('reports')
        context['ReportForm'] = ReportForm()
        return context


@permission_required('reports.delete_reportdefinition', raise_exception=True)
def report_delete(request, pk):
    object = ReportDefinition.objects.get(pk=pk)
    if request.method == 'POST':
        object.delete()
        messages.success(request, 'Se ha eliminado la plantilla del reporte correctamente.')
        return JsonResponse({'ok': True}, safe=False)
    else:
        messages.error(request, 'Eliminación rechazada.')


class ReportInventoryView(ValidatePermissionRequiredMixin, FilterView):
    template_name = 'reports/reports_inventory.html'
    filterset_class = ProductFilter
    permission_required = 'inventory.report_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports')
        return context


def exportProductPDF(request):
    """Example of ExportPDF"""
    products = Product.objects.all()

    products_list = []
    for product in products:
        products_list.append({
            'name': product.name,
            'category': product.category.name,
            'state': product.state,
            'stock': product.stock
        })

    # person = Person.objects.filter(id=1).first()
    data = {
        'products': products_list,
        # 'image': convert_to_64(person.image.url)
    }

    return report(request, 'products', data)
