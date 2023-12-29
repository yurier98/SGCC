from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from ..Mixin.mixins import ValidatePermissionRequiredMixin
from ..models import BlockedIP


class BlockedIPListView(ValidatePermissionRequiredMixin, ListView):
    model = BlockedIP
    template_name = 'blocked_ip/blocked_ip_list.html'
    permission_required = 'view_group'
    url_redirect = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                groups = Group.objects.prefetch_related('permissions')
                data = serializers.serialize('json', groups)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'IP Bloqueados'
        context['title'] = 'Listado de ip bloqueados'
        context['create_url'] = reverse_lazy('group_create')
        context['list_url'] = reverse_lazy('blocked_ip_list')

        context['permissions'] = BlockedIP.objects.all()
        return context
