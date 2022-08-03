import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView
from swapper import load_model

from .forms import EmailForm
from .mixins import EmailMixin

# from .models import Notification


Notification = load_model('notification', 'Notification')


class Index(EmailMixin, TemplateView):
    template_name = 'notifications/notificacion.html'
    email_template_name = 'email.html'

    def get_context_data(self, **kwargs):
        """
        Método para pegar o formulário e os dados submetidos.
        Nota - Customize a estrutura de seu email no arquivo email.html
        """
        context = super(Index, self).get_context_data(**kwargs)
        form = EmailForm()
        # data example
        data = dict()
        data['email_to'] = self.request.POST.get('email_to')
        data['title'] = self.request.POST.get('title')
        data['message'] = self.request.POST.get('message')

        context['form'] = form
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):
        self.send_mail()
        return HttpResponseRedirect(reverse_lazy('notifications_list'))


####################Vistas de Prestamos##################
class NotificationListView(ListView):
    """ Return las notifications del usuario logeado"""
    model = Notification
    paginate_by = 10
    template_name = 'notifications/notifications.html'
    # template_name = 'notifications/notify.html'
    # context_object_name = 'notify'

    # permission_required = 'view_loan'

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'search':
    #             data = []
    #
    #             start_date = request.POST['start_date']
    #             end_date = request.POST['end_date']
    #
    #             a = ['all', 'This week', 'This month', 'last 3 month']
    #
    #             vfilter = a[1]
    #
    #             print(vfilter)
    #
    #             queryset = Notification.objects.all()
    #
    #             if len(start_date) and len(end_date):
    #                 queryset = queryset.filter(created__range=[start_date, end_date])
    #
    #                 start_date=timezone.now().date() - datetime.timedelta(days=1)
    #
    #                 queryset = queryset.filter(created__range=[start_date, end_date])
    #
    #                 thisweek = timezone.now().date() - datetime.timedelta(days=1)
    #
    #                 # self.fechaCreada.date() >= timezone.now().date() - datetime.timedelta(days=1)
    #
    #                 '''
    #                 hacer consulta de los ultmios 3 meses
    #                 queryset = queryset.
    #
    #                 hacer consulta para este mes
    #
    #
    #                 hacer consulta para esta semana
    #
    #
    #                 hacer consulta para todos
    #                  queryset = Notification.objects.all()
    #
    #                 '''
    #
    #             for i in queryset:
    #                 data.append(i.toJSON())
    #
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     except Exception as e:
    #         data['error'] = str(e)
    #         print(e)
    #     return JsonResponse(data, safe=False)

    @method_decorator(login_required)
    def dispatch(self, requets, *args, **kwargs):
        return super(NotificationListView, self).dispatch(requets, *args, **kwargs)

    # def get_queryset(self):
    #     ''' aqui tengo q devolver las notificaciones asociadas al usauario autenticado'''
    #     return self.request.user.notifications.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificaciones'
        context['create_url'] = reverse_lazy('create')
        context['list_url'] = reverse_lazy('loan_list')
        context['entity'] = 'Notificaciones'
        return context
