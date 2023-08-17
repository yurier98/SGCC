from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm

from .models import Product


class ProductoForm(ModelForm):
    class Meta:
        model = Product
        # fields = ['name', 'category', 'img', 'state', 'active', 'stock', 'available']
        # fields = '__all__'
        exclude = ['created', 'updated']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'state': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }),
            'img': forms.FileInput(attrs={
                'class': 'form-control',
            }),

        }
