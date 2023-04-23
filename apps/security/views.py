<<<<<<< HEAD
from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..Forms.groups_forms import GroupsForm
from ..Mixin.mixins import ValidatePermissionRequiredMixin


# Create your views here.


def json(request, self=None):
    # data = list(Permission.objects.values())
    # data = UserProfile.toJSON(self)
    data = []
    perm = Permission.objects.all()
    for i in perm:
        data.append(i)
        print(data)

    return JsonResponse(data, safe=False)


class GroupListView(ValidatePermissionRequiredMixin, ListView):
    model = Group
    template_name = 'groups/list.html'
    permission_required = 'view_group'
    url_redirect = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                data = list(Group.objects.values())
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
        context['title'] = 'Listado de Grupos y Roles'
        context['create_url'] = reverse_lazy('group_create')
        context['list_url'] = reverse_lazy('group_list')
        context['entity'] = 'Grupos'
        return context


class GroupCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupsForm
    template_name = 'groups/create.html'
    success_url = reverse_lazy('group_list')
    url_redirect = success_url
    permission_required = 'add_group'

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear rol'
        context['entity'] = 'Roles'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class GroupUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GroupsForm
    template_name = 'groups/create.html'
    success_url = reverse_lazy('group_list')
    url_redirect = success_url
    permission_required = 'change_group'

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
        context['title'] = 'Modificar Rol'
        context['entity'] = 'Roles'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class GroupDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Group
    template_name = 'groups/delete.html'
    success_url = reverse_lazy('group_list')
    url_redirect = success_url
    permission_required = 'delete_group'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        mensaje = f'{self.model.__name__} eliminado correctamente'
        try:
            self.object.delete()
            # data['error'] = mensaje
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Rol'
        context['entity'] = 'Roles'
        context['list_url'] = self.success_url
        return context
=======
from .Views.views_permission import *
from .Views.views_groups import *
>>>>>>> origin/main
