from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .Forms.groups_forms import GroupsForm
from .Mixin.mixins import ValidatePermissionRequiredMixin


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



from .Views.views_groups import *
from .Views.views_permission import *


