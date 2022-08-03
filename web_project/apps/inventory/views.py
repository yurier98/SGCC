from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView, BSModalCreateView, BSModalUpdateView
from django.db import transaction
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from .filters import ProductFilter
from .forms import ProductoForm, CategoryForm
from .models import Product, Category


# Create your views here.
class ProductFilterView(LoginRequiredMixin, FilterView):
    """ Return un filtrado de  Productos"""
    filterset_class = ProductFilter
    template_name = 'inventory/inventory_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('inventory:inventory')
        context['entity'] = 'Inventario'
        return context


class ProductListView(LoginRequiredMixin, ListView):
    """ Return all Productos"""
    model = Product
    paginate_by = 24
    context_object_name = 'products_list'
    template_name = 'inventory/inventory_list.html'
    redirect_field_name = 'inventory:inventory'

    # add_home = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Inventario'
        return context


class Create(LoginRequiredMixin, CreateView):
    # model = Product
    # exclude = ['created', 'updated']
    # fields = ['name', 'category', 'img','state','active','stock','available']
    # fields = '__all__'
    form_class = ProductoForm
    template_name = 'inventory/create_product.html'
    success_message = 'Producto creada correctamente.'
    success_url = reverse_lazy('inventory:inventory')


class Detail(BSModalReadView, DetailBreadcrumbMixin):
    model = Product
    home_label = _("My new home")
    template_name = 'inventory/detail_product.html'


class Update(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductoForm
    # template_name = 'inventory/update_product.html'
    template_name = 'inventory/editar.html'
    success_message = 'El producto se ha actualizado con exito'
    success_url = reverse_lazy('inventory:inventory')


class Delete(SuccessMessageMixin, BSModalDeleteView):
    model = Product
    template_name = 'inventory/delete_product.html'
    success_message = 'El producto se ha eliminado con exito'
    success_url = reverse_lazy('inventory:inventory')


####################Vistas de Category##################

class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    permission_required = 'view_category'
    url_redirect = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categoría de productos '
        context['create_url'] = reverse_lazy('category_create')
        context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Nomencladores'
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category_list')
    url_redirect = success_url
    permission_required = 'add_category'

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
        context['title'] = 'Crear categoría'
        context['entity'] = 'Nomencladores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CategoryUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category_list')
    url_redirect = success_url
    permission_required = 'change_category'

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
        context['title'] = 'Modificar categoría'
        context['entity'] = 'Nomencladores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CategoryDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('category_list')
    url_redirect = success_url
    permission_required = 'delete_category'

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
        context['title'] = 'Eliminar categoría'
        context['entity'] = 'Nomencladores'
        context['list_url'] = self.success_url
        return context

#################### FIN Vistas de Manifestación##################
