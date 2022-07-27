from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin
from .models import Loan, Manifestation
from ..accounts.models import UserProfile
from datetime import datetime


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class LoanForm(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all().filter(is_active=True)
        self.fields['description'].widget.attrs['rows'] = 3

    class Meta:
        model = Loan
        # fields = '__all__'
        exclude = ['start_date', 'end_date', 'created', 'updated']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'manifestation': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
                # 'style': 'width: 100%'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                # 'class': 'form-control',
                'style': 'height: 100px',

                'class': 'form-control',
                'rows': 3,
                'cols': 3
            }),

            # 'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
            #     'value': datetime.now().strftime('%Y-%m-%d'),
            #     'autocomplete': 'off',
            #     'class': 'form-control datetimepicker-input',
            #     'id': 'date_joined',
            #     'data-target': '#date_joined',
            #     'data-toggle': 'datetimepicker'
            # }),

        }


class ManifestationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Manifestation
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
