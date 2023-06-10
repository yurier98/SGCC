from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm

from .models import Product


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Product
        #fields = ['name', 'category', 'img', 'state', 'active', 'stock', 'available']
        #fields = '__all__'
        exclude = ['created', 'updated']

