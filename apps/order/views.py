import json
import os

from crum import get_current_request
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
# Create your views here.
from django.template.loader import get_template
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView
from weasyprint import HTML, CSS
from django.urls import reverse_lazy, resolve, reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, View, DetailView

from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin, ExistsInventaryMixin, GroupRequiredMixin, \
    IsSuperuserMixin, GroupNotAllowedMixin
from apps.accounts.models import UserProfile
from apps.loan.models import Loan
from .filters import OrderFilter
from .forms import ReportForm, OrderForm, OrderFormApprove
from .models import Order, OrderProduct, Manifestation
from apps.inventory.models import Product
from apps.notification.signals import notificar


####################Vistas de Pedidos##################
class OrderListAllView(GroupRequiredMixin, ExistsInventaryMixin, FilterView, ListView):
    """ Return all Order"""
    model = Order
    template_name = 'order/order_list.html'
    paginate_by = 10

    filterset_class = OrderFilter
    # permission_required = 'order.view_all_order'
    url_redirect = reverse_lazy('order_list')
    group_names = ['tecnico', 'admin']
    redirect_field_name = 'order_list'

    # permission_required = 'view_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de pedidos'
        context['create_url'] = reverse_lazy('order_create')
        context['list_url'] = reverse_lazy('order_all_list')
        context['entity'] = 'Todos los Pedidos'
        context['stats'] = self.model.stats
        return context


class OrderListView(GroupNotAllowedMixin, ExistsInventaryMixin, LoginRequiredMixin, FilterView):
    """ Return all Order of usuario"""
    filterset_class = OrderFilter
    paginate_by = 10
    is_paginated = True
    template_name = 'order/order_list.html'
    permission_required = 'order.view_order'
    url_redirect = reverse_lazy('order_list')

    disallowed_group = 'tecnico'
    error_url = 'order_all_list'

    # permission_required = 'view_order'
    # Modificar el metodo getQuery para hacer una comprobacion de q sea los pedidos del usuario autenticado

    def get_queryset(self):
        queryset = Order.objects.filter(user__username=get_current_request().user, is_delete=False)
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


class OrderCreateView(ExistsInventaryMixin, LoginRequiredMixin, GroupNotAllowedMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'add_order'

    disallowed_group = 'tecnico'
    error_url = 'order_all_list'

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
                    # filtrar por estado prestado (P)
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
                    order.user_id = int(request.POST['user'])
                    order.description = request.POST['description']
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
                    messages.success(request, 'Se ha creado el pedido exitosamente.')
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


class OrderUpdateView(LoginRequiredMixin, GroupNotAllowedMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'change_order'
    disallowed_group = 'tecnico'
    error_url = 'order_all_list'

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = OrderForm(instance=instance)
        form.fields['user'].queryset = UserProfile.objects.filter(id=instance.user.id)
        return form

    def get_details_product(self):
        data = []
        order = self.get_object()
        for i in order.products.all():
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
                        order.products.all().delete()
                        for i in products:
                            detail = OrderProduct()
                            detail.order_id = order.id
                            detail.product_id = int(i['id'])
                            detail.cant = int(i['cant'])

                            detail.save()
                            detail.product.stock -= detail.cant
                            detail.product.save()
                        data = {'id': order.id}
                    messages.success(request, 'Se ha modificado el pedido exitosamente.')
                    data = {'id': order.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['products'] = self.get_details_product()
        return context


class OrderDetailView(LoginRequiredMixin, DetailView, SingleObjectMixin):
    model = Order
    template_name = 'order/order_detail.html'
    success_url = reverse_lazy('order_list')
    url_redirect = success_url
    permission_required = 'view_order'

    def get_details_product(self):
        data = []
        order = self.get_object()
        for i in order.products.all():
            item = i.product.toJSON()
            item['cant'] = i.cant
            data.append(item)
        return json.dumps(data)

    def get_next_object(self):
        # Obtener el objeto actual
        object = self.get_object()

        # Obtener una lista de objetos con estado 'pendiente'
        objects = Order.objects.filter(state='Pendiente').order_by('-created')

        # Obtener el índice del objeto actual en la lista
        current_index = 0
        for i, obj in enumerate(objects):
            if obj.id == object.id:
                current_index = i
                break
        # Obtener el siguiente objeto en la lista
        next_object = None
        if current_index < len(objects) - 1:
            next_object = objects[current_index + 1]

        return next_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del pedido'
        context['entity'] = 'Pedidos'
        # context['action'] = 'edit'
        context['products'] = self.get_details_product()

        # context['list_url'] = self.success_url
        user = self.request.user
        if user.groups.filter(name='tecnico').exists():
            context['list_url'] = reverse('order_all_list')
            # Obtener el próximo objeto con estado 'pendiente'
            next_object = self.get_next_object()
            # Agregar la URL del próximo objeto al contexto
            if next_object:
                context['next_object_url'] = reverse('order_detail', args=[next_object.pk])

        else:
            context['list_url'] = reverse('order_list')

        return context


class OrderUpdatePermissionView(ValidatePermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderFormApprove
    template_name = 'order/order_create.html'
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
        for i in order.products.all():
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
                        order.products.all().delete()
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
                            messages.error(request, 'El pedido no ha sido aprobado 😕.')
                        if state.__eq__('Aprobado'):
                            lo = Loan.objects.create(user_id=int(request.POST['user']),
                                                     start_date=request.POST['start_date'],
                                                     end_date=request.POST['end_date'],
                                                     description=request.POST['description'],
                                                     state='PR',
                                                     manifestation_id=int(request.POST['manifestation']),
                                                     )
                            # LoanProduct.objects.create(loan=lo, product_id=int(i['id']), cant=int(i['cant']), )
                            notificar.send(user, destiny=user, verb='😀 Se ha aprobado su pedido.',
                                           level='success')
                            messages.success(request, 'El pedido ha sido aprobado 😀.')

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
    # url_redirect = reverse_lazy('order_all_list')
    permission_required = 'approve_order'

    def get(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        order = Order.objects.get(pk=self.kwargs['pk'])
        user = order.user
        prev_url = request.META.get('HTTP_REFERER', reverse('order_all_list'))
        try:
            # if request.user.has_perm('order.approve_order'):
            if request.user.has_perm('order.approve_order'):
                if current_url.__eq__('order_approve'):
                    order.state = 'Aprobado'
                    order.save()
                    Loan.objects.create(state='PE', order_id=order.id, )
                    notificar.send(user, destiny=user, verb='😀 Se ha aprobado su pedido.',
                                   level='success')
                    messages.success(request, 'El pedido ha sido aprobado 😀.')
                    print('😀 Se ha aprobado ...')
                elif current_url.__eq__('order_deny'):
                    order.state = 'No Aprobado'
                    order.save()
                    notificar.send(user, destiny=user, verb='😕 Se denegado la aprobación de su pedido.',
                                   level='info')
                    messages.error(request, 'El pedido no ha sido aprobado 😕.')

        except:
            pass
        return redirect(prev_url)
