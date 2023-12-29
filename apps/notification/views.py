import datetime

from crum import get_current_request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

# Create your views here.
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from swapper import load_model
from django.contrib import messages
from django.core.mail import send_mail
from apps.loan.models import Loan
from django.contrib.auth import get_user_model
# from apps.accounts.models import UserProfile

from .signals import notificar
from .forms import EmailForm
from .mixins import EmailMixin
from .models import SystemNotification, EmailNotification

User = get_user_model()


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


####################Vistas de Notification##################
class NotificationListView(ListView):
    """ Return las notifications del usuario logeado"""
    model = SystemNotification
    paginate_by = 10
    template_name = 'notifications/notifications.html'
    context_object_name = 'notifications'

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
    #                 queryset = queryset.filter(timestamp__range=[start_date, end_date])
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

    def get(self, request):
        queryset = self.get_queryset()
        time_period = request.GET.get('time_period')

        if time_period == 'last_week':
            filtered_queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(days=2))
        elif time_period == 'last_month':
            filtered_queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
        elif time_period == 'last_3_months':
            filtered_queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(days=90))
        else:
            filtered_queryset = queryset

        self.object_list = filtered_queryset
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)

    def get_queryset(self):
        queryset = SystemNotification.objects.filter(user__username=get_current_request().user, is_delete=False)
        # queryset.update(read=True)  # cambiar esta propiedad para q solo cumpla por la paginacion
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Notificaciones'
        context['title'] = ' Listado de notificaciones'
        return context


# class NotificationViewSet(viewsets.ModelViewSet):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     filter_backends = (SearchFilter,)
#     search_fields = ('verb', 'description')
#
#     def get_queryset(self):
#         return self.request.user.notifications.filter(timestamp__lte=datetime.now()).order_by('-timestamp', '-unread')
#
#
#     def get_today(self, request):
#         today = datetime.now().today()
#         results = self.get_queryset().filter(timestamp__year=today.year, timestamp__month=today.month,
#                                              timestamp__day=today.day)
#         return results
#
#
#     def get_yesterday(self, request):
#         yesterday = datetime.now().today() - datetime.timedelta(days=1)
#         results = self.get_queryset().filter(timestamp__year=yesterday.year, timestamp__month=yesterday.month,
#                                              timestamp__day=yesterday.day)
#         return results
#
#
#     def get_last_month(self, request):
#         now = datetime.now().today()
#         previous_month = datetime.now().today() - datetime.timedelta(days=30)
#         results = self.get_queryset().filter(timestamp__range=(previous_month, now))
#
#         return results
#
#     def get_last_year(self, request):
#         now = datetime.now().today()
#         previous_year = datetime.now().today() - datetime.timedelta(days=256)
#         results = self.get_queryset().filter(timestamp__range=(previous_year, now))
#         return results
#
#     @action(url_path='mte/get_unread_count', detail=False)
#     def get_unread_count(self, request):
#         try:
#             results = {
#                 'count': request.user.notifications.filter(timestamp__lte=datetime.now(), unread=True).count(),
#                 "cancel_notifications": not request.user.profile.be_notified
#             }
#             return Response(results)
#         except Notification.DoesNotExist:
#             pass
#
#     @action(url_path='mark_all_as_read', detail=False)
#     def mark_all_as_read(self, request, pk=None):
#         results = request.user.notifications.filter(unread=True)
#         results.update(unread=False)
#         return Response({'status': status.HTTP_200_OK})


class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        form = EmailForm()
        loan = Loan.objects.get(pk=self.kwargs['pk'])
        user = loan.order.user.pk
        if user:
            email = User.objects.get(id=user).email
        context = {
            'form': form,
            'email_value': email,
            'title': 'Enviar correo electrónico',
            'entity': 'Préstamos'
        }
        return render(request, 'notifications/notify_by_email.html', context)

    def post(self, request, **kwargs):
        print('Entrando al post')
        form = EmailForm(request.POST)
        if form.is_valid():
            print('form valido')
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            email_to = [form.cleaned_data['email_to']]
            from_email = 'ztazhorde@gmail.com'
            print('antes del try')
            try:
                print('dentor del try enviando correo')
                response = send_mail(subject, body, from_email, email_to)
                print('respuesta', response)
                messages.success(request, 'Correo electrónico enviado con éxito.')
                loan = Loan.objects.get(pk=self.kwargs['pk'])
                user = User.objects.get(id=loan.order.user.pk)
                notificar.send(sender=self.__class__, user=user,
                               message='Se le ha enviado un correo electrónico con información sobre un préstamo',
                               level='info')
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")

        return redirect('loan_list')


class SendEmailView2(SuccessMessageMixin, CreateView):
    model = EmailNotification
    form_class = EmailForm
    template_name = 'notifications/notify_by_email.html'
    success_message = 'Correo electrónico enviado con éxito.'
    success_url = reverse_lazy('loan_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Préstamos'
        context['title'] = 'Enviar correo electrónico'
        context['list_url'] = self.success_url
        return context


class SendEmailViewTest(View):
    def get(self, request, **kwargs):
        form = EmailForm()
        loan = Loan.objects.get(pk=self.kwargs['pk'])
        user = loan.order.user.pk
        if user:
            email = User.objects.get(id=user).email
        context = {
            'form': form,
            'email_value': email,
            'title': 'Enviar correo electrónico',
            'entity': 'Préstamos'
        }
        return render(request, 'loan/notify_by_email.html', context)

    def post(self, request, **kwargs):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            to_email = [form.cleaned_data['email_to']]
            from_email = 'ztazhorde@gmail.com'

            try:
                send_mail(subject, message, from_email, to_email)
                messages.success(request, "Correo enviado con éxito.")
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")

        return redirect('loan_list')


@require_http_methods(['POST'])
def delete_notification(request, pk):
    # remove the film from the user's list
    my_object = SystemNotification.objects.get(pk=pk)
    my_object.is_delete = True
    my_object.save()

    notifications = SystemNotification.objects.filter(user__username=get_current_request().user,
                                                      is_delete=False).order_by('-created_at')

    return render(request, 'notifications/partials/notification-list.html', {'notifications': notifications})

@require_http_methods(['POST'])
def mark_all_as_read(request, pk=None):
    results = request.user.notifications.filter(read=False)
    results.update(read=True)
    # return Response({'status': status.HTTP_200_OK})
    return render(request, 'notifications/partials/notification-list.html')
