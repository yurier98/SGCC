from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from .models import Loan
from ..accounts.models import UserProfile
from datetime import datetime


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class PrestamoForm(ModelForm):
    class Meta:
        model = Loan
        # fields = '__all__'
        exclude = ['created', 'updated']

        labels = {
            'fechaini': 'Fecha de inicio',
            'fechafin': 'Fecha de entrega',
            'descripcion': 'Descripcion',
            'manifestacion': 'Manifestacion',

        }

        widgets = {
            'user': AutocompleteSelect(
                UserProfile._meta.get_field('user').remote_field,
                admin.site,
                attrs={'placeholder': 'seleccionar...'},
            ),
        }
        #
        # help_texts = {
        #
        #     'fecha': 'Formato de la fecha dd/mm/yyyy',
        #     'hora': 'Formato de la hora 01:50:30',
        # }
        # error_messages = {
        #     'fecha': {
        #         'max_length': ("El formato de la fecha es incorrecto ejemplo : 01/12/2020."),
        #     }
        # }


class LoanForm(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all()
        self.fields['description'].widget.attrs['rows'] = 3

    class Meta:
        model = Loan
        # fields = '__all__'
        exclude = ['created', 'updated']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'custom-select select2',
                #'style': 'width: 100%'
            }),
            'manifestation': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
                # 'style': 'width: 100%'
            }),
            # 'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
            #     'value': datetime.now().strftime('%Y-%m-%d'),
            #     'autocomplete': 'off',
            #     'class': 'form-control datetimepicker-input',
            #     'id': 'date_joined',
            #     'data-target': '#date_joined',
            #     'data-toggle': 'datetimepicker'
            # }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'row': 3,
                'style': 'width: 100%'


            })
        }
