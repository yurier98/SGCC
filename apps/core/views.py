from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView
from apps.inventory.models import Product
from apps.loan.models import Loan
from apps.order.models import Order


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

