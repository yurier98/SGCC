from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django_filters.views import FilterView

from .models import Rule, Trace
from .forms import RuleForm
from .filters import TraceFilter


class TracesListView(LoginRequiredMixin, FilterView, ListView):
    model = Trace
    template_name = 'audit/traces_list.html'
    context_object_name = 'traces_list'
    paginate_by = 10
    filterset_class = TraceFilter

    # queryset = Trace.objects.order_by('-timestamp')

    # def get_details_traces(self):
    #     trace = Trace.objects.get(pk=self.kwargs['pk'])
    #     print(trace)
    #     return trace

    def get_details_traces(self, request, pk):
        trace = get_object_or_404(Trace, pk=pk)
        if request.is_ajax():
            return JsonResponse({'detalles': trace.user})
            # return render(request, 'audit/traces_details.html', {'registro': registro})
        return render(request, 'audit/traces_details.html', {'registro': trace})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Auditorias'
        context['title'] = 'Listado de trazas'
        context['list_url'] = reverse_lazy('traces_list')
        context['filter'] = TraceFilter(self.request.GET, queryset=self.get_queryset())
        # context['details'] = self.get_details_traces()
        return context

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        trace = Trace.objects.get(id=id)
        print(trace)
        return JsonResponse({'ok': True, 'trace': trace.to_JSON()}, safe=False)


@require_POST
def validate_rule_form(request):
    ruleForm = RuleForm(request.POST)

    if ruleForm.is_valid():
        return JsonResponse({'success': True})
    else:
        errors = ruleForm.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})


class RuleListView(LoginRequiredMixin, ListView):
    model = Rule
    template_name = 'audit/rule_list.html'
    context_object_name = 'rule_list'

    # def post(self, request, *args, **kwargs):
    #     try:
    #         action = request.POST['action']
    #         if action == 'createRule':
    #             rule = Rule()
    #             rule.is_active = True if request.POST.get('is_active') == 'on' else False
    #             rule.check_create = True if request.POST.get('check_create') == 'on' else False
    #             rule.check_edit = True if request.POST.get('check_edit') == 'on' else False
    #             rule.check_delete = True if request.POST.get('check_delete') == 'on' else False
    #             rule.content_type = ContentType.objects.get(pk=request.POST['content_type'])
    #             rule.save()
    #             messages.success(request, 'La Regla ha sido creada con éxito.')
    #
    #         elif action == 'editRule':
    #             rule = Rule.objects.get(id=request.POST['id'])
    #             rule.is_active = True if request.POST.get('is_active') == 'on' else False
    #             rule.check_create = True if request.POST.get('check_create') == 'on' else False
    #             rule.check_edit = True if request.POST.get('check_edit') == 'on' else False
    #             rule.check_delete = True if request.POST.get('check_delete') == 'on' else False
    #             rule.content_type = ContentType.objects.get(pk=request.POST['content_type'])
    #             rule.save()
    #             messages.success(request, 'La Regla ha sido editada con éxito.')
    #         else:
    #             messages.error(request, 'Ocurrio un error.')
    #     except Exception as e:
    #         messages.error(request, str(e))
    #     return redirect(reverse_lazy('rule_list'))

    def post(self, request, *args, **kwargs):
        rule_id = request.POST.get('id')

        if rule_id:
            # Se proporcionó un identificador, por lo que se está actualizando una regla existente
            print('Actualizar regla')
            instance = Rule.objects.get(id=rule_id)
            rule_form = RuleForm(request.POST, instance=instance)
            if rule_form.is_valid():
                rule_form.save()
                messages.success(request, 'La Regla ha sido editada con éxito.')
            else:
                print(rule_form.errors)
                messages.error(request, 'Formulario inválido.')
        else:
            # No se proporcionó un identificador, por lo que se está creando una nueva regla
            ruleForm = RuleForm(request.POST)
            if ruleForm.is_valid():
                ruleForm.save()
                messages.success(request, 'La Regla ha sido creada con éxito.')
            else:
                messages.error(request, 'Formulario inválido.')

        return redirect('rule_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Auditorias'
        context['title'] = 'Listado de reglas'
        context['list_url'] = reverse_lazy('traces_list')
        context['RuleForm'] = RuleForm()
        return context


# class DeleteOldTraces(CronJobBase):
#     RUN_EVERY_MINS = 1440  # Ejecutar cada 24 horas
#
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'trazas.delete_old_traces'  # un nombre único
#
#     def do(self):
#         deadline = datetime.now() - timedelta(days=90)  # Fecha límite de 3 meses
#         Trace.objects.filter(date__lte=deadline).delete()

def createregla(request):
    return render(request, 'audit/rule_create.html', {})


def eliminartraza(request, pk):
    traza = Trace.objects.get(id=pk)
    if request.method == 'POST':
        traza.delete()
        return JsonResponse({'ok': True}, safe=False)
    else:
        return render(request, 'audit/traces_delete.html', {'traza': traza})


def eliminarregla(request, pk):
    regla = Rule.objects.get(id=pk)
    if request.method == 'POST':
        regla.delete()
        return JsonResponse({'ok': True}, safe=False)
    else:
        return render(request, 'audit/rule_delete.html', {'x': regla})


def viewtraza(request, pk):
    traza = Trace.objects.get(id=pk)
    return render(request, 'audit/traces_details.html', {'traza': traza})
