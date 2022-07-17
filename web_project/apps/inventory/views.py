from bootstrap_modal_forms.generic import BSModalDeleteView, BSModalReadView, BSModalCreateView, BSModalUpdateView
from django.utils.translation import gettext_lazy as _
from view_breadcrumbs import DetailBreadcrumbMixin, ListBreadcrumbMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .forms import ProductoForm
from .models import Product


# Create your views here.


class ProductListView(LoginRequiredMixin, ListView):
    """ Return all Productos"""
    model = Product
    # paginate_by = 10  # El número de objetos que se mostrarán por página, en este caso queremos que se muestren 3 Convocatorias por página.
    context_object_name = 'products_list'
    template_name = 'inventory/inventory_list.html'
    # add_home = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        # context['create_url'] = reverse_lazy('create')
        # context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Inventario'
        return context


class Create(LoginRequiredMixin, CreateView):
    #model = Product
    #exclude = ['created', 'updated']
    #fields = ['name', 'category', 'img','state','active','stock','available']
    # fields = '__all__'
    form_class = ProductoForm
    template_name = 'inventory/create_product.html'
    success_message = 'Producto creada correctamente.'
    success_url = reverse_lazy('inventory:inventory')


class Detail(BSModalReadView,DetailBreadcrumbMixin):
    model = Product
    home_label = _("My new home")
    template_name = 'inventory/detail_product.html'


class Update(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductoForm
    #template_name = 'inventory/update_product.html'
    template_name = 'inventory/editar.html'
    success_message = 'El producto se ha actualizado con exito'
    success_url = reverse_lazy('inventory:inventory')


class Delete(SuccessMessageMixin, BSModalDeleteView):
    model = Product
    template_name = 'inventory/delete_product.html'
    success_message = 'El producto se ha eliminado con exito'
    success_url = reverse_lazy('inventory:inventory')
