from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.forms import ModelForm

from .models import Product


class ProductoForm(ModelForm):
    class Meta:
        model = Product
        # fields = ['name', 'category', 'img', 'state', 'active', 'stock', 'available']
        # fields = '__all__'
        exclude = ['created_at', 'updated']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%'
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

    # def clean_img(self):
    #     image = self.cleaned_data.get('img')
    #     if image:
    #         if image.size > 2 * 1024 * 1024:  # Tamaño máximo permitido: 2MB
    #             raise forms.ValidationError("El tamaño de la imagen no puede exceder los 2MB.")
    #         if not image.content_type.startswith('image/'):  # Solo se permiten imágenes
    #             raise forms.ValidationError("El archivo seleccionado no es una imagen.")
    #     else:
    #         return None
    #     return image
