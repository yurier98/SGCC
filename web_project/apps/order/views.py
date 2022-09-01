import json
import os

from crum import get_current_request
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.template.loader import get_template
from django_filters.views import FilterView
from weasyprint import HTML, CSS
from django.urls import reverse_lazy, resolve
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, View

from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin, ExistsInventaryMixin, IsSuperuserMixin
from apps.accounts.models import UserProfile
from apps.loan.models import Loan, LoanProduct
from .filters import OrderFilter
from .forms import ReportForm, OrderForm, OrderFormApprove
from .models import Order, OrderProduct
from apps.inventory.models import Product
from apps.notification.signals import notificar


####################Vistas de Pedidos##################
class OrderListAllView(ExistsInventaryMixin, ValidatePermissionRequiredMixin, FilterView):
    """ Return all Order"""
    filterset_class = OrderFilter
    template_name = 'order/list_order.html'
    permission_required = 'order.view_order'
    url_redirect = reverse_lazy('order_list')

    # permission_required = 'view_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de pedidos'
        context['create_url'] = reverse_lazy('order_create')
        context['list_url'] = reverse_lazy('order_list')
        context['entity'] = 'Pedidos'
        return context


class OrderListView(ExistsInventaryMixin, LoginRequiredMixin, FilterView):
    """ Return all Order"""
    filterset_class = OrderFilter
    paginate_by = 2
    is_paginated = True
    template_name = 'order/list_order.html'
    permission_required = 'order.view_order'
    url_redirect = reverse_lazy('order_list')

    # permission_required = 'view_order'
    # Modificar el metodo getQuery para hacer una comprobacion de q sea los pedidos del usuario autenticado

    def get_queryset(self):
        queryset = Order.objects.filter(user__username=get_current_request().user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de mis pedidos'
        context['create_url'] = reverse_lazy('order_create')
        context['list_url'] = reverse_lazy('order_list')
        context['entity'] = 'Mis Pedidos'
        return context


class OrderListView2(ExistsInventaryMixin, LoginRequiredMixin, FormView):
    """ Return all Order"""
    form_class = ReportForm
    template_name = 'order/list.html'
    permission_required = 'view_loan'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Order.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(created__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_products_detail':
                data = []
                for i in OrderProduct.objects.filter(loan_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de pedidos'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Pedidos'
        return context


class OrderCreateView(ExistsInventaryMixin, LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/create.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'add_order'

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
                    # filtrar por es estado prestado (P)
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
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    order = Order()
                    order.start_date = request.POST['start_date']
                    order.end_date = request.POST['end_date']

                    # user = UserProfile.objects.values().filter(id=get_current_request().user.id)
                    # print(user)
                    # order.user_id = int(user)
                    order.user_id = int(request.POST['user'])

                    order.description = request.POST['description']
                    # loan.state = request.POST['state']
                    order.manifestation_id = int(request.POST['manifestation'])

                    order.save()
                    for i in products:
                        detail = OrderProduct()
                        detail.order_id = order.id
                        detail.product_id = int(i['id'])
                        detail.cant = int(i['cant'])
                        detail.save()
                        detail.product.stock -= detail.cant
                        detail.product.save()
                    user = Order.objects.get(pk=order.pk).user
                    notificar.send(user, destiny=user, verb='Se ha creado un pedido a su usuario exitosamente.',
                                   level='info')
                    data = {'id': order.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hacer pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['products'] = []
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/create.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'change_order'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = OrderForm(instance=instance)
        form.fields['user'].queryset = UserProfile.objects.filter(id=instance.user.id)
        return form

    def get_details_product(self):
        data = []
        order = self.get_object()
        for i in order.orderproduct_set.all():
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
                        order = self.get_object()
                        order.start_date = request.POST['start_date']
                        order.end_date = request.POST['end_date']
                        order.user_id = int(request.POST['user'])
                        order.description = request.POST['description']
                        order.manifestation_id = int(request.POST['manifestation'])
                        order.save()
                        order.orderproduct_set.all().delete()
                        for i in products:
                            detail = OrderProduct()
                            detail.order_id = order.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])

                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        data = {'id': order.id}
                    data = {'id': order.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aprobación del pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        return context


class OrderUpdatePermissionView(ValidatePermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderFormApprove
    template_name = 'order/create.html'
    success_url = reverse_lazy('all_order_list')
    url_redirect = success_url
    permission_required = {'order.approve_order', 'order.change_order'}

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = OrderFormApprove(instance=instance)
        form.fields['user'].queryset = UserProfile.objects.filter(id=instance.user.id)
        return form

    def get_details_product(self):
        data = []
        order = self.get_object()
        for i in order.orderproduct_set.all():
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
                        order = self.get_object()
                        order.start_date = request.POST['start_date']
                        order.end_date = request.POST['end_date']
                        order.user_id = int(request.POST['user'])
                        order.description = request.POST['description']
                        state = request.POST['state']
                        order.state = state
                        order.manifestation_id = int(request.POST['manifestation'])
                        order.save()
                        order.orderproduct_set.all().delete()
                        for i in products:
                            detail = OrderProduct()
                            detail.order_id = order.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])

                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        user = UserProfile.objects.get(id=request.POST['user'])
                        if state.__eq__('No Aprobado'):
                            notificar.send(user, destiny=user, verb='😕 Se denegado la aprobación de su pedido.',
                                           level='info')
                        if state.__eq__('Aprobado'):
                            lo = Loan.objects.create(user_id=int(request.POST['user']),
                                                     start_date=request.POST['start_date'],
                                                     end_date=request.POST['end_date'],
                                                     description=request.POST['description'],
                                                     state='PR',
                                                     manifestation_id=int(request.POST['manifestation']),
                                                     )
                            LoanProduct.objects.create(loan=lo,
                                                       product_id=int(i['id']),
                                                       cant=int(i['cant']),
                                                       )
                            notificar.send(user, destiny=user, verb='😀 Se ha aprobado su pedido.',
                                           level='success')

                        data = {'id': order.id}
                    data = {'id': order.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Aprobación del pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        return context


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'delete_loan'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        order = Order.objects.get(pk=self.kwargs['pk'])
        user = order.user
        try:
            notificar.send(user, destiny=user, verb='⚠ Se ha eliminado su pedido.',
                           level='wrong')
            self.object.delete()

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar un pedido'
        context['entity'] = 'Pedido'
        context['list_url'] = self.success_url
        return context


class OrderPdfView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('order/invoice.html')
            context = {
                'object': Order.objects.get(pk=self.kwargs['pk']),
                'icon': f'{settings.STATIC_URL}assets/images/app-logo.svg'
            }
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('loan_list'))


#################### FIN Vistas de Pedido##################

class ApproveView(ValidatePermissionRequiredMixin, View):
    url_redirect = reverse_lazy('all_order_list')
    permission_required = 'approve_order'

    def get(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        order = Order.objects.get(pk=self.kwargs['pk'])
        user = order.user
        try:
            # if request.user.has_perm('order.approve_order'):
            if request.user.has_perm('order.approve_order'):
                if current_url.__eq__('order_approve'):

                    order.state = 'Aprobado'
                    order.save()
                    lo = Loan.objects.create(user_id=order.user_id, start_date=order.start_date,
                                             end_date=order.end_date,
                                             description=order.description, state='PR',
                                             manifestation_id=order.manifestation_id,
                                             )
                    orderProduct = OrderProduct.objects.get(order=order)
                    LoanProduct.objects.create(loan=lo, product_id=orderProduct.product_id, cant=orderProduct.cant)
                    notificar.send(user, destiny=user, verb='😀 Se ha aprobado su pedido.',
                                   level='success')
                    print('😀 Se ha aprobado ...')
                elif current_url.__eq__('order_deny'):
                    order.state = 'No Aprobado'
                    order.save()
                    notificar.send(user, destiny=user, verb='😕 Se denegado la aprobación de su pedido.',
                                   level='info')
                    print('😕 Se denegado la aprobación de su pedido.')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('all_order_list'))
