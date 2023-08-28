from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView, BSModalCreateView, BSModalUpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin
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
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('inventory_list')
        context['entity'] = 'Inventario'
        return context


class ProductListView(ValidatePermissionRequiredMixin, FilterView, ListView):
    """ Return all Productos"""
    model = Product
    paginate_by = 24
    filterset_class = ProductFilter

    # context_object_name = 'products_list'
    template_name = 'inventory/inventory_list.html'
    redirect_field_name = 'inventory_list'
    permission_required = 'inventory.view_product'

    # add_home = False

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     data = {'productos': []}
    #     for producto in queryset:
    #         data['productos'].append({
    #             'nombre': producto.name,
    #             'imagen': producto.img.url if producto.img else '',
    #             # Agregar aquí más campos que quieras mostrar en la tarjeta
    #         })
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Inventario'
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


class ProductCreateView(ValidatePermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ProductoForm
    template_name = 'inventory/create_product.html'
    success_message = 'Producto creada correctamente.'

    success_url = reverse_lazy('inventory_list')
    url_redirect = success_url
    permission_required = 'inventory.add_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear producto'
        context['entity'] = 'Inventario'
        context['list_url'] = self.success_url
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/detail_product.html'
    url_redirect = reverse_lazy('inventory_list')

    # permission_required = 'view_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del producto'
        context['entity'] = 'Inventario'
        context['list_url'] = self.url_redirect
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductoForm
    template_name = 'inventory/product_update.html'
    success_url = reverse_lazy('inventory_list')

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar producto'
        context['entity'] = 'Inventario'
        context['list_url'] = self.success_url
        context['url_detail'] = reverse_lazy('product_detail')
        context['list_update'] = reverse_lazy('product_update')
        context['action'] = 'edit'
        return context


# class Detail(BSModalReadView, DetailBreadcrumbMixin):
#     model = Product
#     home_label = _("My new home")
#     template_name = 'inventory/detail_product.html'


class Update(ValidatePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductoForm

    template_name = 'inventory/editar.html'
    success_message = 'El producto se ha actualizado con exito'
    success_url = reverse_lazy('inventory:inventory')
    permission_required = 'inventory.add_product'


class Delete(SuccessMessageMixin, BSModalDeleteView):
    model = Product
    template_name = 'inventory/delete_product.html'
    success_message = 'El producto se ha eliminado con exito'
    success_url = reverse_lazy('inventory:inventory')


class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('inventory_list')
    success_message = 'El producto se ha eliminado con exito.'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        if self.request.is_ajax():
            return JsonResponse({'message': 'Object deleted successfully.'})
        else:
            return super().delete(request, *args, **kwargs)
