from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy, resolve, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView, RedirectView, DetailView
from django_filters.views import FilterView
from apps.security.Mixin.mixins import ValidatePermissionRequiredMixin
from .models import UserProfile
from .filters import UserFilter
from .forms import UserForm, UserProfileForm

# Create your views here.

MODULE_NAME = 'Cuentas'

#   Vistas de los Usuarios que solo tiene acceso el admin ######
class UserListView(ValidatePermissionRequiredMixin, FilterView, ListView):
    model = UserProfile
    template_name = 'user/user_list.html'
    permission_required = 'view_userprofile'
    filterset_class = UserFilter

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                for i in UserProfile.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = MODULE_NAME
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user_create')
        context['list_url'] = reverse_lazy('user_list')

        return context


class UserCreateView(ValidatePermissionRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'add_userprofile'
    url_redirect = success_url

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
        context['entity'] = MODULE_NAME
        context['title'] = 'Crear Usuario'

        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class UserUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'

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
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificar usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'

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
        context['title'] = 'Eliminación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context


#   Vistas de los Usuarios del sistema ######
class UserUpdateProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user/profile_update.html'
    success_url = reverse_lazy('profile_details')

    def get_object(self, queryset=None):
        return self.request.user

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
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDetailProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user/profile_details.html'

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del perfil'
        context['entity'] = 'Perfil'
        # context['list_url'] = self.success_url

        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = UserProfile
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de Password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeactivateView(ValidatePermissionRequiredMixin, View):
    permission_required = 'approve_order'

    def get(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).url_name
        user = UserProfile.objects.get(pk=self.kwargs['pk'])
        prev_url = request.META.get('HTTP_REFERER', reverse('user_list'))
        try:
            if request.user.has_perm('order.approve_order'):
                if current_url.__eq__('user_desactivate'):
                    user.is_active = False
                    user.save()
                    messages.warning(request, 'El usuario ha sido desactivado.')
                elif current_url.__eq__('user_activate'):
                    user.is_active = True
                    user.save()
                    messages.warning(request, 'El usuario ha sido activado.')
        except:
            pass
        return redirect(prev_url)
