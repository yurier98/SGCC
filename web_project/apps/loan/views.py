import json
import os
from bootstrap_modal_forms.generic import BSModalReadView, BSModalDeleteView, BSModalFormView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView

from ..accounts.models import UserProfile
from .forms import ReportForm, LoanForm
from .models import Loan, LoanProduct
from ..inventory.models import Product


class LoanListView(FormView):
    """ Return all Prestamos"""
    form_class = ReportForm
    template_name = 'loan/list.html'
    permission_required = 'view_loan'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Loan.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(created__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_products_detail':
                data = []
                for i in LoanProduct.objects.filter(loan_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Préstamos'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Préstamos'
        return context


class LoanCreateView(CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan/create.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'add_loan'
    success_message = 'Préstamo creado correctamente.'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                products = Product.objects.filter(stock__gt=0)
                if len(term):
                    products = products.filter(name__icontains=term)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    loan = Loan()
                    # loan.created = request.POST['created']
                    start_date = request.POST['start_date']
                    end_date = request.POST['end_date']
                    # loan.start_date = request.POST['start_date']
                    print(start_date, end_date)
                    loan.start_date = start_date
                    # loan.end_date = end_date
                    loan.user_id = int(request.POST['user'])
                    loan.description = request.POST['description']
                    loan.state = request.POST['state']
                    loan.manifestation_id = int(request.POST['manifestation'])
                    # loan.iva = float(request.POST['iva'])
                    loan.save()
                    for i in products:
                        detail = LoanProduct()
                        detail.loan_id = loan.id
                        detail.product_id = int(i['id'])
                        detail.cant = int(i['cant'])
                        detail.save()
                        detail.product.stock -= detail.cant
                        detail.product.save()
                    data = {'id': loan.id}
            elif action == 'search_user':
                data = []
                term = request.POST['term']
                # filtrar por el usurio o el solapin arreglar el JS para poner la descripcion del solapin
                users = UserProfile.objects.filter(
                    Q(user__username__icontains=term) | Q(solapin__icontains=term))[0:10]
                for i in users:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Préstamo'
        context['entity'] = 'Préstamo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        return context


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


class Search_Producto(generic.ListView, BSModalFormView):
    model = Product
    context_object_name = 'productos'
    template_name = 'loan/search_product.html'


class Create(LoginRequiredMixin, CreateView):
    form_class = LoanForm
    template_name = 'loan/create_loan.html'
    success_message = 'Préstamo creado correctamente.'  # Mostramos este Mensaje luego de Crear una reservacion
    success_url = reverse_lazy('loan:list')

    # def form_valid(self, form):
    #     form.instance.usuario = self.request.user
    #     return super().form_valid(form)


class Detail(BSModalReadView):
    model = Loan
    template_name = 'loan/detail_loan.html'


class Update(LoginRequiredMixin, UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan/update_loan.html'
    success_message = 'El préstamo se ha actualizado con exito'
    success_url = reverse_lazy('loan:list')


class Delete(SuccessMessageMixin, BSModalDeleteView):
    model = Loan
    template_name = 'loan/delete_loan.html'
    success_message = 'El préstamo se ha eliminado con exito'
    success_url = reverse_lazy('loan:list')


class LoanPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('loan/invoice.html')
            context = {
                'loan': Loan.objects.get(pk=self.kwargs['pk']),
                'icon': f'{settings.MEDIA_URL}logo.png'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('loan_list'))


class LoanDeleteView(DeleteView):
    model = Loan
    template_name = 'loan/delete.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'delete_loan'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Préstamo'
        context['entity'] = 'Préstamos'
        context['list_url'] = self.success_url
        return context


class LoanUpdateView(UpdateView):
    model = Loan
    # form_class = SaleForm
    # template_name = 'sale/create.html'
    # success_url = reverse_lazy('sale_list')
    # url_redirect = success_url
    # permission_required = 'change_sale'
    #
    # def get_form(self, form_class=None):
    #     instance = self.get_object()
    #     form = SaleForm(instance=instance)
    #     form.fields['user'].queryset = UserProfile.objects.filter(id=instance.client.id)
    #     return form
    #
    # def get_details_product(self):
    #     data = []
    #     sale = self.get_object()
    #     for i in sale.saleproduct_set.all():
    #         item = i.product.toJSON()
    #         item['cant'] = i.cant
    #         data.append(item)
    #     return json.dumps(data)
    #
    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'search_products':
    #             data = []
    #             ids_exclude = json.loads(request.POST['ids'])
    #             term = request.POST['term'].strip()
    #             products = Product.objects.filter(stock__gt=0)
    #             if len(term):
    #                 products = products.filter(name__icontains=term)
    #             for i in products.exclude(id__in=ids_exclude)[0:10]:
    #                 item = i.toJSON()
    #                 item['value'] = i.name
    #                 # item['text'] = i.name
    #                 data.append(item)
    #         elif action == 'search_products_select2':
    #             data = []
    #             ids_exclude = json.loads(request.POST['ids'])
    #             term = request.POST['term'].strip()
    #             data.append({'id': term, 'text': term})
    #             products = Product.objects.filter(name__icontains=term, stock__gt=0)
    #             for i in products.exclude(id__in=ids_exclude)[0:10]:
    #                 item = i.toJSON()
    #                 item['text'] = i.__str__()
    #                 data.append(item)
    #         elif action == 'edit':
    #             with transaction.atomic():
    #                 with transaction.atomic():
    #                     products = json.loads(request.POST['products'])
    #                     sale = self.get_object()
    #                     sale.date_joined = request.POST['date_joined']
    #                     sale.client_id = int(request.POST['client'])
    #                     sale.iva = float(request.POST['iva'])
    #                     sale.save()
    #                     sale.saleproduct_set.all().delete()
    #                     for i in products:
    #                         detail = SaleProduct()
    #                         detail.sale_id = sale.id
    #                         detail.product_id = int(i['id'])
    #                         detail.cant = int(i['cant'])
    #                         detail.price = float(i['pvp'])
    #                         detail.subtotal = detail.cant * detail.price
    #                         detail.save()
    #                         detail.product.stock -= detail.cant
    #                         detail.product.save()
    #                     sale.calculate_invoice()
    #                     data = {'id': sale.id}
    #                 data = {'id': sale.id}
    #         elif action == 'search_client':
    #             data = []
    #             term = request.POST['term']
    #             clients = Client.objects.filter(
    #                 Q(names__icontains=term) | Q(dni__icontains=term))[0:10]
    #             for i in clients:
    #                 item = i.toJSON()
    #                 item['text'] = i.get_full_name()
    #                 data.append(item)
    #         elif action == 'create_client':
    #             with transaction.atomic():
    #                 form = ClientForm(request.POST)
    #                 data = form.save()
    #         else:
    #             data['error'] = 'No ha ingresado a ninguna opción'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Edición de una Venta'
    #     context['entity'] = 'Ventas'
    #     context['list_url'] = self.success_url
    #     context['action'] = 'edit'
    #     context['products'] = self.get_details_product()
    #     context['frmClient'] = ClientForm()
    #     return context
