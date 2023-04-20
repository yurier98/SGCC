from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from apps.inventory.models import Product
from apps.loan.models import Loan
from apps.order.models import Order
from apps.core.models import Manifestation
from apps.core.forms import ManifestationForm


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "index_default.html"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Administradores').exists():
                template_name = 'admin_index.html'
            elif self.request.user.groups.filter(name='Tecnicos').exists():
                template_name = 'tecnicos_index.html'
            elif self.request.user.groups.filter(name='Superusuario').exists():
                template_name = 'superuser_index.html'
            else:
                template_name = 'unknown_group_index.html'
        else:
            template_name = 'anonymous_index.html'

        return [template_name]

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        loanp = Loan.objects.all().filter(state='PR')
        cont = 0
        for i in loanp:
            date = i.order.end_date
            if date.today() > date:
                cont += 1
        context['title'] = 'Inicio'
        context['cantProductos'] = Product.objects.all().count()
        context['totalLoan'] = Loan.objects.all().count()
        context['loanpendiente'] = Loan.objects.all().filter(state='PR').count()
        context['orderPendiente'] = Order.objects.all().filter(state='Pendiente').count()
        context['loanFaltantes'] = cont
        return context


def custom_permission_denied_view(request, exception=None):
    '''
    Estamos obteniendo la URL de la página anterior usando request.META.get('HTTP_REFERER')
    y guardándola en la variable referer. Luego, estamos creando un diccionario de contexto
    que incluye la variable referer y pasándolo a la función render.
    '''
    referer = request.META.get('HTTP_REFERER')
    context = {
        'referer': referer,
    }
    return render(request, 'error/403.html', context, status=403)


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
