from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

from apps.order.models import Order
from .models import Loan
from apps.accounts.models import UserProfile
from datetime import datetime


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'btn app-btn-secondary dropdown-toggle',
    }))


class LoanForm(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    state_loan = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select',
                                                              # 'style': 'width: 100%'
                                                              }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all().filter(is_active=True)
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['state_loan'].choices = Loan.STATE
        # self.fields['state'].choices = Order.STATE[1:2]

    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['state', 'created', 'updated']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'manifestation': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'class': 'form-control',
                'style': 'height: 100px',
                'rows': 3,
                'cols': 3
            }),
        }
