from django.forms import ModelForm
from django import forms
from .models import Order
from ..accounts.models import UserProfile
from datetime import datetime
from crum import get_current_request


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class OrderForm(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all().filter(id=get_current_request().user.id)
        self.fields['description'].widget.attrs['rows'] = 3

    class Meta:
        model = Order
        # fields = '__all__''
        exclude = ['start_date', 'end_date', 'created', 'updated', 'state']
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


class OrderFormApprove(ModelForm):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all().filter(id=get_current_request().user.id)
        self.fields['description'].widget.attrs['rows'] = 3

    class Meta:
        model = Order
        # fields = '__all__''
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
                'class': 'form-control',
                'style': 'height: 100px',
                'rows': 3,
                'cols': 3
            }),

        }
