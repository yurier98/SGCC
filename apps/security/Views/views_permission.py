from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..Mixin.mixins import ValidatePermissionRequiredMixin


# Create your views here.


class PermissionListView(ValidatePermissionRequiredMixin, ListView):
    model = Permission
    template_name = 'permissions/list.html'
    permission_required = 'view_permission'
    url_redirect = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                data = list(Permission.objects.values())
                grupos = Group.objects.all()
                # for i in grupos:
                #
                #     data.append(i.id,)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Permisos'
        context['create_url'] = reverse_lazy('permission_list')
        context['list_url'] = reverse_lazy('permission_list')
        context['entity'] = 'Permisos'
        return context
