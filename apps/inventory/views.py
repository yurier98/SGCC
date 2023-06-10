from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView, BSModalCreateView, BSModalUpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

# from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from ..security.Mixin.mixins import ValidatePermissionRequiredMixin
from .filters import ProductFilter
from .forms import ProductoForm
from .models import Product, Category


# Create your views here.
class ProductFilterView(ValidatePermissionRequiredMixin, FilterView):
    """ Return un filtrado de  Productos"""
    filterset_class = ProductFilter
    template_name = 'inventory/inventory_list.html'
    permission_required = 'inventory.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('inventory:inventory')
        context['entity'] = 'Inventario'
        return context


class ProductListView(ValidatePermissionRequiredMixin, ListView):
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


class ProductCreateView(ValidatePermissionRequiredMixin, CreateView):

    form_class = ProductoForm
    template_name = 'inventory/create_product.html'
    success_message = 'Producto creada correctamente.'
    success_url = reverse_lazy('inventory:inventory')
    url_redirect = success_url
    permission_required = 'inventory.add_product'


# class Detail(BSModalReadView, DetailBreadcrumbMixin):
#     model = Product
#     home_label = _("My new home")
#     template_name = 'inventory/detail_product.html'


class Update(ValidatePermissionRequiredMixin, UpdateView):
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


