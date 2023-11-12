import json
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import get_template
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from weasyprint import HTML, CSS
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, View, DetailView
from .forms import ReportForm, LoanForm
from .models import Loan
from .filters import LoanFilter
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin, ExistsInventaryMixin
from apps.accounts.models import UserProfile
from apps.order.models import Order, OrderProduct
from apps.inventory.models import Product
from apps.notification.signals import notificar


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = get_template('index.html')
    return HttpResponse(html_template.render(context, request))


####################Vistas de Prestamos##################

class LoanListView(ValidatePermissionRequiredMixin, FilterView, ListView):
    model = Loan
    filterset_class = LoanFilter
    # paginate_by = 10
    template_name = 'loan/loan_list.html'
    permission_required = 'loan.view_loan'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     start_date = self.request.GET.get('start_date')
    #     end_date = self.request.GET.get('end_date')
    #     if start_date and end_date:
    #         start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
    #         end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
    #         queryset = queryset.filter(order__created__range=[start_date, end_date])
    #     return queryset
    def get_queryset(self):
        return Loan.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Préstamos'
        context['title'] = 'Listado de Préstamos'
        context['create_url'] = reverse_lazy('loan_create')
        context['list_url'] = reverse_lazy('loan_list')
        context['filter'] = LoanFilter(self.request.GET, queryset=self.get_queryset())
        context['stats'] = self.model.stats()
        return context

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         action = form.cleaned_data['action']
    #         if action == 'search':
    #             loans = self.get_queryset()
    #             data = [loan.toJSON() for loan in loans]
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     else:
    #         data['error'] = form.errors
    #     return JsonResponse(data, safe=False)


class LoanListView2(ExistsInventaryMixin, ValidatePermissionRequiredMixin, FormView):
    """ Return all Prestamos"""
    form_class = ReportForm
    template_name = 'loan/list.html'
    permission_required = 'loan.view_loan'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                loan = Loan.objects.all()

                # queryset = loan.get(order__created=)
                # queryset = loan.filter(order__created__range=[start_date, end_date])
                # queryset = Order.objects.all()

                if len(start_date) and len(end_date):
                    queryset = loan.filter(order__created__range=[start_date, end_date])
                    # queryset = queryset.filter(created__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
                    print(data)
            elif action == 'search_products_detail':
                data = []
                for i in OrderProduct.objects.filter(order_id=request.POST['order.id']):
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
        context['create_url'] = reverse_lazy('loan_create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Préstamos'
        return context


class LoanCreateView(ExistsInventaryMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan/loan_create.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'loan.add_loan'

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
                    # excluir de la consulta los productos con estado prestado (P)
                for i in products.exclude(id__in=ids_exclude).exclude(state__exact='P')[0:10]:
                    item = i.toJSON()
                    item['value'] = i.__str__()
                    data.append(item)
            elif action == 'search_products_select2':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                data.append({'id': term, 'text': term})
                products = Product.objects.filter(name__icontains=term, stock__gt=0)
                for i in products.exclude(id__in=ids_exclude).exclude(state__exact='P')[0:10]:
                    item = i.toJSON()
                    item['te  xt'] = i.__str__()
                    data.append(item)
            elif action == 'search_user':
                data = []
                term = request.POST['term']
                # filtrar por el usuario o el solapin arreglar el JS para poner la descripción del solapin
                users = UserProfile.objects.filter(
                    Q(user__username__icontains=term) | Q(solapin__icontains=term))[0:10]
                for i in users:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])

                    order = Order()
                    order.start_date = request.POST['start_date']
                    order.end_date = request.POST['end_date']
                    order.user_id = int(request.POST['user'])
                    order.description = request.POST['description']
                    order.state = Order.State.APROBADO
                    order.manifestation_id = int(request.POST['manifestation'])
                    order.save()

                    loan = Loan()
                    loan.order_id = order.id
                    loan.state = request.POST['state_loan']

                    for i in products:
                        order_product = OrderProduct()
                        order_product.order_id = order.id
                        order_product.product_id = int(i['id'])
                        order_product.cant = int(i['cant'])
                        order_product.save()

                        # order_product.product.stock -= order_product.cant
                        # if order_product.product.stock == 0:
                        #     order_product.product.state = 'P'
                        # order_product.product.save()

                        # product = Product.objects.get(pk=i['id'])
                        # product.stock = int(product.stock) - int(i['cant'])
                        # if product.stock == 0:
                        #     product.state = 'P'
                        # product.save()


                    if loan.state == 'Prestado':
                        products_order_loan = loan.order.products.all()
                        for i in products_order_loan:

                            # order_product.product.stock -= order_product.cant
                            # if order_product.product.stock == 0:
                            #     order_product.product.state = 'P'
                            # order_product.product.save()

                            i.product.stock -= i.cant
                            if i.product.stock == 0:
                                i.product.state = 'P'
                            i.product.save()

                    loan.save()


                    # user = UserProfile.objects.get(id=request.POST['user'])
                    user = Order.objects.get(pk=order.pk).user
                    notificar.send(user, destiny=user, verb='Se ha creado un préstamo a su usuario exitosamente, '
                                                            'para recogerlo contacte con nosotros.',
                                   level='info')
                    messages.success(request, '¡Préstamo guardado con éxito!')

                    data = {'id': order.id}
                    # detail = OrderProduct()
                    # detail.order_id = order.id
                    # detail.product_id = int(i['id'])
                    # detail.cant = int(i['cant'])
                    # detail.save()
                    # detail.product.stock -= detail.cant
                    # detail.product.save()
                    # data = {'id': loan.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear préstamo'
        context['entity'] = 'Préstamos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        return context


class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan/loan_create.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'change_loan'

    def get_form(self, form_class=None):
        instance = self.get_object().order
        form = LoanForm(instance=instance)
        form.fields['user'].queryset = UserProfile.objects.filter(id=instance.user.id)
        form.fields['state_loan'].initial = self.get_object().state

        return form

    def get_details_product(self):
        data = []
        loan = self.get_object()
        for i in loan.order.products.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        return json.dumps(data)

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
                    item['value'] = i.name
                    # item['text'] = i.name
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
            elif action == 'search_user':
                data = []
                term = request.POST['term']
                users = UserProfile.objects.filter(
                    Q(user__username__icontains=term) | Q(solapin__icontains=term))[0:10]
                for i in users:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    with transaction.atomic():
                        products = json.loads(request.POST['products'])
                        loan = self.get_object()
                        loan.state = request.POST['state_loan']
                        loan.save()

                        for i in products:
                            order_product = OrderProduct()
                            order_product.order_id = loan.order.id
                            order_product.product_id = i['id']
                            order_product.quantity = i['cant']
                            order_product.save()
                            product = Product.objects.get(pk=i['id'])
                            if loan.state == Loan.State.ENTREGADO:
                                product.stock = int(product.stock) + int(i['cant'])
                                product.state = 'D'
                            product.save()

                            messages.success(request, '¡Préstamo editado con éxito!')
                        data['id'] = loan.id
                        # data = {'id': loan.id}
                    data['id'] = loan.id
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificar préstamo'
        context['entity'] = 'Préstamo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        # context['frmClient'] = ClientForm()
        return context


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
        context['title'] = 'Eliminar Préstamo'
        context['entity'] = 'Préstamos'
        context['list_url'] = self.success_url
        return context


class LoanDetailView(DetailView):
    model = Loan
    template_name = 'loan/loan_detail.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'view_loan'

    def get_details_product(self):
        data = []
        loan = self.get_object()
        for i in loan.order.products.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del préstamo'
        context['entity'] = 'Préstamos'
        context['list_url'] = self.success_url
        context['products'] = self.get_details_product()
        return context


class LoanPdfView(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('loan/invoice.html')
            context = {
                'loan': Loan.objects.get(pk=self.kwargs['pk']),
                'icon': f'{settings.STATIC_URL}assets/images/app-logo.svg'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('loan_list'))

#################### FIN Vistas de Préstamos##################
