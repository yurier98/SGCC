import json
import os
from bootstrap_modal_forms.generic import BSModalReadView, BSModalDeleteView, BSModalFormView, BSModalCreateView, \
    BSModalUpdateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, View

from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin, ExistsInventaryMixin, IsSuperuserMixin
from apps.accounts.models import UserProfile
from .forms import ReportForm, LoanForm, ManifestationForm
from .models import Loan, LoanProduct, Manifestation
from apps.inventory.models import Product


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = get_template('index.html')
    return HttpResponse(html_template.render(context, request))


####################Vistas de Prestamos##################
class LoanListView(ExistsInventaryMixin, ValidatePermissionRequiredMixin, FormView):
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


class LoanCreateView(ExistsInventaryMixin, ValidatePermissionRequiredMixin, CreateView):
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
                    #filtrar por es estado prestado (P)
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
                for i in products.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
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
                    loan = Loan()
                    loan.start_date = request.POST['start_date']
                    loan.end_date = request.POST['end_date']
                    loan.user_id = int(request.POST['user'])
                    loan.description = request.POST['description']
                    loan.state = request.POST['state']
                    loan.manifestation_id = int(request.POST['manifestation'])
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
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear préstamo'
        context['entity'] = 'Préstamo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
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
        context['title'] = 'Eliminación de un Préstamo'
        context['entity'] = 'Préstamos'
        context['list_url'] = self.success_url
        return context


class LoanUpdateView(UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loan/create.html'
    success_url = reverse_lazy('loan_list')
    url_redirect = success_url
    permission_required = 'change_loan'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = LoanForm(instance=instance)
        form.fields['user'].queryset = UserProfile.objects.filter(id=instance.user.id)
        return form

    def get_details_product(self):
        data = []
        loan = self.get_object()
        for i in loan.loanproduct_set.all():
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
                        loan.start_date = request.POST['start_date']
                        loan.end_date = request.POST['end_date']
                        loan.user_id = int(request.POST['user'])
                        loan.description = request.POST['description']
                        loan.state = request.POST['state']
                        loan.manifestation_id = int(request.POST['manifestation'])
                        loan.save()
                        loan.loanproduct_set.all().delete()
                        for i in products:
                            detail = LoanProduct()
                            detail.loan_id = loan.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])

                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        data = {'id': loan.id}
                    data = {'id': loan.id}
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

####################Vistas de Manifestación##################

class ManifestationListView(ListView):
    model = Manifestation
    template_name = 'manifestation/list.html'
    permission_required = 'view_manifestation'
    url_redirect = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Manifestation.objects.all():
                    data.append(i.toJSON())
            elif action == 'create_manifestation':
                with transaction.atomic():
                    form = ManifestationForm(request.POST)
                    print(form)
                    data = form.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Manifestaciones'
        context['create_url'] = reverse_lazy('manifestation_create')
        context['list_url'] = reverse_lazy('manifestation_list')
        context['entity'] = 'Manifestaciones'
        context['frmManifestation'] = ManifestationForm()
        return context


class ManifestationCreateView(CreateView):
    model = Manifestation
    form_class = ManifestationForm
    template_name = 'manifestation/create.html'
    success_url = reverse_lazy('manifestation_list')
    url_redirect = success_url
    permission_required = 'add_manifestation'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear manifestación'
        context['entity'] = 'Manifestaciones'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ManifestationUpdateView(UpdateView):
    model = Manifestation
    form_class = ManifestationForm
    template_name = 'manifestation/create.html'
    success_url = reverse_lazy('manifestation_list')
    url_redirect = success_url
    permission_required = 'change_manifestation'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificar Categoría'
        context['entity'] = 'Manifestation'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ManifestationDeleteView(BSModalDeleteView):
    model = Manifestation
    template_name = 'manifestation/delete.html'
    success_url = reverse_lazy('manifestation_list')
    url_redirect = success_url
    permission_required = 'delete_manifestation'

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
        context['title'] = 'Eliminar Manifestación'
        context['entity'] = 'Manifestación'
        context['list_url'] = self.success_url
        return context

#################### FIN Vistas de Manifestación##################
