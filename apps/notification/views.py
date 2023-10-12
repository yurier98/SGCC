import datetime

from crum import get_current_request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView
from swapper import load_model

from .forms import EmailForm, NotificationFilterForm
from .mixins import EmailMixin


#Notification = load_model('notification', 'Notification')


#class Index(EmailMixin, TemplateView):
    #template_name = 'notifications/notificacion.html'
    #email_template_name = 'email.html'

    #def get_context_data(self, **kwargs):
      #  """
      #  Método para pegar o formulário e os dados submetidos.
      #  Nota - Customize a estrutura de seu email no arquivo email.html
      #  """
       # context = super(Index, self).get_context_data(**kwargs)
      #  form = EmailForm()
        # data example
       # data = dict()
       # data['email_to'] = self.request.POST.get('email_to')
        #data['title'] = self.request.POST.get('title')
        #data['message'] = self.request.POST.get('message')

       # context['form'] = form
        #context['data'] = data
       # return context

  #  def post(self, request, *args, **kwargs):
       # self.send_mail()
       # return HttpResponseRedirect(reverse_lazy('notifications_list'))


####################Vistas de Notification##################
#class NotificationListView(ListView):
   # """ Return las notifications del usuario logeado"""
   # model = Notification
    #paginate_by = 10
    #template_name = 'notifications/notifications.html'

    # template_name = 'notifications/notify.html'###3 no quitar de comentarios
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

   # @method_decorator(login_required)
   # def dispatch(self, requets, *args, **kwargs):
      #  return super(NotificationListView, self).dispatch(requets, *args, **kwargs)

    # def get_queryset(self):
    #     ''' aqui tengo q devolver las notificaciones asociadas al usauario autenticado'''
    #     return self.request.user.notifications.all()

   # def get_queryset(self):
        #queryset = Notification.objects.filter(destiny=get_current_request().user)
       # return queryset

   # def get_context_data(self, **kwargs):
       # context = super().get_context_data(**kwargs)
        #context['title'] = 'Notificaciones'
        #context['create_url'] = reverse_lazy('create')
        #context['list_url'] = reverse_lazy('loan_list')
        #context['entity'] = 'Notificaciones'
        #return context


#class NotificationListViewFilter(FormView):
  #  """ Return all the Notifications"""
   # form_class = NotificationFilterForm
   # template_name = 'notifications/notifications.html'

 #
    #def post(self, request, *args, **kwargs):
      #  data = {}
   #try:
   #         action = request.POST['action']
   #         if action == 'search':
   #             data = []
   #             start_date = request.POST['start_date']
   #             end_date = request.POST['end_date']
    #            queryset = Notification.objects.all()
    #            if len(start_date) and len(end_date):
   #                 queryset = queryset.filter(created__range=[start_date, end_date])
   #             for i in queryset:
   #                 data.append(i.toJSON())
   #         elif action == 'delete':
   #             data = []
   #             for i in Notification.objects.filter(id=request.POST['id']):
   #                 data.append(i.toJSON())
                    # Toamar el objeto y cambiarle el estado a eliminado


  #          elif action == 'search_products_detail':
   #             data = []
   #             for i in Notification.objects.filter(loan_id=request.POST['id']):
  #                  data.append(i.toJSON())
   #         else:
  #              data['error'] = 'Ha ocurrido un error'
  #      except Exception as e:
  #          data['error'] = str(e)
       #     print(e)
   #     return JsonResponse(data, safe=False)

  #  def get_context_data(self, **kwargs):
  #      context = super().get_context_data(**kwargs)
   #     context['title'] = 'Listado de Notificaciones'
  #      context['create_url'] = reverse_lazy('loan_create')
   #     context['list_url'] = reverse_lazy('loan_list')
  #      context['entity'] = 'Notificaciones'
   #     return context


# class NotificationViewSet(viewsets.ModelViewSet):## esat calse se mnatiene comentariada
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
#class NotificationDetailView(LoginRequiredMixin, DetailView):
   # #model = Notification
   # template_name = 'notifications/notification_detail.html'
   # success_url = reverse_lazy('notifications_list')
    #url_redirect = success_url

   # def get(self, request, *args, **kwargs):
        #self.object = self.get_object()
       # notify = Notification.objects.get(pk=self.kwargs['pk'])
        #try:
           # notify.read = True
          #  notify.save()
     #   except:
           # pass
       # context = self.get_context_data(object=self.object)
       # return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     form = DetailForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # Write Your Logic here
    #
    #         self.object = self.get_object()
    #         context = super(Detail, self).get_context_data(**kwargs)
    #         context['form'] = DetailForm
    #         return self.render_to_response(context=context)
    #
    #     else:
    #         self.object = self.get_object()
    #         context = super(NotificationDetailView, self).get_context_data(**kwargs)
    #         context['form'] = form
    #         return self.render_to_response(context=context)


  #  def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
     #   context['title'] = 'Detalles de la notificación'
      #  context['entity'] = 'Notificaciones'
       # context['list_url'] = self.success_url
        # context['action'] = 'edit'
        # context['products'] = self.get_details_product()
       # return context

##### a partir de aqui cambios ###########
from django.views.generic import ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from .models import EmailNotification, SystemNotification

class NotificationListView(ListView):
    model = SystemNotification
    paginate_by = 10
    template_name = 'notifications/notifications.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # Filtrar notificaciones por fecha
    #     time_filter = self.request.GET.get("time_filter")
    #     if time_filter == "last_week":
    #         queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(weeks=1))
    #     elif time_filter == "last_month":
    #         queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(weeks=4))
    #     elif time_filter == "last_three_months":
    #         queryset = queryset.filter(created_at__gte=timezone.now() - timezone.timedelta(weeks=12))
    #     return queryset

    def get_queryset(self):
        queryset = SystemNotification.objects.filter(user__username=get_current_request().user, is_delete=False)
        return queryset

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'delete':
    #             messages.success(request, "La notificación no fue eliminada.")
    #
    #         elif action == 'mark_read':
    #
    #             messages.success(request, "La notificación.")
    #
    #         else:
    #             messages.error(request, "Hubo un error.")
    #     except Exception as e:
    #         data['error'] = str(e)
    #         print(e)
    #     return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de notificaciones'
        context['entity'] = 'Notificaciones'
        return context




# success_url = reverse_lazy('notifications_list')
# url_redirect = success_url

# def get(self, request, *args, **kwargs):
# self.object = self.get_object()
# notify = Notification.objects.get(pk=self.kwargs['pk'])
# try:
# notify.read = True
#  notify.save()
#   except:
# pass
# context = self.get_context_data(object=self.object)
# return self.render_to_response(context)

# def post(self, request, *args, **kwargs):
#     form = DetailForm(request.POST, request.FILES)
#     if form.is_valid():
#         # Write Your Logic here
#
#         self.object = self.get_object()
#         context = super(Detail, self).get_context_data(**kwargs)
#         context['form'] = DetailForm
#         return self.render_to_response(context=context)
#
#     else:
#         self.object = self.get_object()
#         context = super(NotificationDetailView, self).get_context_data(**kwargs)
#         context['form'] = form
#         return self.render_to_response(context=context)


#  def get_context_data(self, **kwargs):
#    context = super().get_context_data(**kwargs)
#   context['title'] = 'Detalles de la notificación'
#  context['entity'] = 'Notificaciones'
# context['list_url'] = self.success_url
# context['action'] = 'edit'
# context['products'] = self.get_details_product()
# return context


class NotificationDeleteView(DeleteView): ## ver por ahi otra forma de eliminar
    model = SystemNotification
    success_url = reverse_lazy("notification_list")
    template_name = "notification_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            messages.success(request, "La notificación no fue eliminada.")
            return self.get(request, *args, **kwargs)
        else:
            messages.success(request, "La notificación fue eliminada.")
            return super().post(request, *args, **kwargs)

class NotificationBulkDeleteView(DeleteView):
    model = SystemNotification
    success_url = reverse_lazy("notification_list")
    template_name = "notification_bulk_delete.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            messages.success(request, "Las notificaciones no fueron eliminadas.")
            return self.get(request, *args, **kwargs)
        else:
            ids = request.POST.getlist("ids")
            self.model.objects.filter(id__in=ids).delete()
            messages.success(request, "Las notificaciones  fueron eliminadas.")
            return self.get(request, *args, **kwargs)

class ExpiredNotificationDeleteView(DeleteView):
    model = SystemNotification

    def get(self, request, *args, **kwargs):
        self.model.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(weeks=12)).delete()
        return super().get(request, *args, **kwargs)