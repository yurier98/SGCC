from datetime import datetime

from crum import get_current_request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.utils.http import urlencode

from apps.inventory.models import Product


class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'Usted no tiene permiso de superusuario.')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('home')
        return self.url_redirect

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request = get_current_request()
        '''No se le puede asignar los permisos al super usuario q acceda a todos los modulos solo a los roles'''
        # if request.user.is_superuser:
        #     return super().get(request, *args, **kwargs)
        '''get_all_permissions => Devuelve una lista con los permisos que tiene concedidos un usuario, ya sea 
        a través de los grupos a los que pertenece o bien asignados directamente.'''
        perms_user = request.user.get_all_permissions()
        if perms_user:
            perms_required = self.get_perms()
            # print(request.user.has_perms(perms_required))
            if request.user.has_perms(perms_required) == False:
                messages.error(request, 'No tiene permiso para ingresar a este módulo')
                return HttpResponseRedirect(self.get_url_redirect())
            return super().get(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())


class ExistsInventaryMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if Product.objects.all().filter(active=True).exists():
            return super().dispatch(request, *args, **kwargs)
        messages.warning(request, 'No se puede continuar si no hay productos en el inventario')
        return redirect('home')





class GroupRequiredMixin(UserPassesTestMixin):
    """
    Mixin que verifica si el usuario actual pertenece a uno o varios grupos.
    """
    group_names = None  # Lista de nombres de grupos requeridos
    redirect_field_name = None  # Nombre del campo de redirección

    def test_func(self):
        """
        Verifica si el usuario actual pertenece a uno o varios grupos.
        """
        user = self.request.user
        if user.is_authenticated and self.group_names:
            return user.groups.filter(name__in=self.group_names).exists()
        return False

    def get_login_url(self):
        """
        Devuelve la URL a la que se redireccionará al usuario si no tiene permisos.
        """
        if self.redirect_field_name:
            query_string = urlencode({self.redirect_field_name: self.request.path})
            messages.error(self.request, 'No tiene permiso para acceder a este recurso.')
            return f"{reverse_lazy('login')}?{query_string}"
        else:
            return reverse_lazy('login')

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class GroupNotAllowedMixin(UserPassesTestMixin):
    """
    Mixin que verifica si el usuario actual NO pertenece a un grupo específico.
    Si el usuario pertenece al grupo, se redirecciona a una página de error.
    """
    disallowed_group = None  # Nombre del grupo no permitido
    error_url = None  # URL de la página de error

    def test_func(self):
        """
        Verifica si el usuario actual NO pertenece al grupo específico.
        """
        user = self.request.user
        if user.is_authenticated and self.disallowed_group:
            return not user.groups.filter(name=self.disallowed_group).exists()
        return False

    def handle_no_permission(self):
        """
        Redirecciona al usuario a la página de error indicada si pertenece al grupo no permitido.
        """
        messages.error(self.request, 'No tiene permiso para realizar esta acción.')

        return redirect(self.error_url)
