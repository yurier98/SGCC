from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm

from .models import Product, Category


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Product
        #fields = ['name', 'category', 'img', 'state', 'active', 'stock', 'available']
        #fields = '__all__'
        exclude = ['created', 'updated']


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre para la categoría'}),
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
