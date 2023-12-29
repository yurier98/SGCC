from django.shortcuts import render
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.inventory.models import Category
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from apps.nomenclatures.models import Manifestation
from apps.nomenclatures.forms import ManifestationForm, CategoryForm
# Create your views here.


####################Vistas de Manifestación##################

class ManifestationListView(ValidatePermissionRequiredMixin, ListView):
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


class ManifestationCreateView(ValidatePermissionRequiredMixin, CreateView):
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


class ManifestationUpdateView(ValidatePermissionRequiredMixin, UpdateView):
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


class ManifestationDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Manifestation
    template_name = 'manifestation/delete.html'
    success_url = reverse_lazy('manifestation_list')
    url_redirect = success_url
    permission_required = 'delete_manifestation'
    success_message = 'Reservación creada correctamente.'

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



####################Vistas de Category##################

class CategoryListView(ValidatePermissionRequiredMixin, ListView):
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


class CategoryCreateView(ValidatePermissionRequiredMixin, CreateView):
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

#################### FIN Vistas de Category##################
