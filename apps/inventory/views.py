from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView, BSModalCreateView, BSModalUpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin
from django_filters.views import FilterView
from django.contrib import messages
# from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from ..security.Mixin.mixins import ValidatePermissionRequiredMixin
from .filters import ProductFilter
from .forms import ProductoForm
from .models import Product, Category

MODULE_NAME = 'Inventario'


# Create your views here.

class ProductListView(ValidatePermissionRequiredMixin, FilterView, ListView):
    """ Return all Productos"""
    model = Product
    paginate_by = 24
    filterset_class = ProductFilter
    template_name = 'inventory/inventory_list.html'
    redirect_field_name = 'inventory_list'
    permission_required = 'inventory.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('inventory_list')
        return context


class ProductCreateView(ValidatePermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ProductoForm
    template_name = 'inventory/create_product.html'
    success_message = 'Producto creada correctamente.'
    success_url = reverse_lazy('inventory_list')
    url_redirect = success_url
    permission_required = 'inventory.add_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Crear producto'
        context['list_url'] = self.success_url
        return context


from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.http import JsonResponse, HttpRequest
from .models import Product


class JsonProductListView(TemplateView, MultipleObjectMixin):
    template_name = 'inventory/inventory_list.html'
    paginate_by = 10
    context_object_name = 'products_list'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if self.request.is_ajax(request):
            data = {'productos': []}
            for producto in self.object_list:
                data['productos'].append({
                    'nombre': producto.name,
                    'imagen': producto.img.url if producto.img else '',
                    # Agregar aquí más campos que quieras mostrar en la tarjeta
                })
            return JsonResponse(data)
        else:
            return self.render_to_response(context)

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Inventario'
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/detail_product.html'
    url_redirect = reverse_lazy('inventory_list')

    # permission_required = 'view_product'
    # permission_required = 'inventory.view_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Detalles del producto'
        context['list_url'] = self.url_redirect
        return context


class ProductUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductoForm
    template_name = 'inventory/product_update.html'
    success_url = reverse_lazy('inventory_list')
    permission_required = 'inventory.change_product'
    success_message = 'El producto se ha actualizado con exito'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Editar producto'
        context['list_url'] = self.success_url
        context['url_detail'] = reverse_lazy('product_detail')
        context['list_update'] = reverse_lazy('product_update')
        context['action'] = 'edit'
        return context


@permission_required('delete_product')  # Comprobar xq da error
def product_delete(request, pk):
    object = Product.objects.get(pk=pk)
    if request.method == 'POST':
        object.delete()
        messages.success(request, 'Se ha eliminado el producto correctamente.')
        return JsonResponse({'ok': True}, safe=False)
    else:
        return render(request, 'inventory/delete_product.html', {'order': object})
