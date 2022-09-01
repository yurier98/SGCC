from datetime import datetime

from crum import get_current_request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# from core.pos.models import Company
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

        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        # metodo obsoleto
        # if 'group' in request.session:
        #     group = request.session['group']
        #     print(group)
        #     perms = self.get_perms()
        #     for p in perms:
        #         if not group.permissions.filter(codename=p).exists():
        #             messages.error(request, 'No tiene permiso para ingresar a este módulo')
        #             return HttpResponseRedirect(self.get_url_redirect())
        #     return super().get(request, *args, **kwargs)
        # messages.error(request, 'No tiene permiso para ingresar a este módulo')
        # return HttpResponseRedirect(self.get_url_redirect())

        '''get_all_permissions => Devuelve una lista con los permisos que tiene 
            concedidos un usuario, ya sea a través de los grupos 
            a los que pertenece o bien asignados directamente.'''
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
        messages.error(request, 'No se puede continuar si no hay productos en el inventario')
        return redirect('home')
