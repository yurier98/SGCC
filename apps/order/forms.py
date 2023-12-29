import json
from urllib import request

from django.contrib import messages
from django.db import transaction
from django.forms import ModelForm
from django import forms
from .models import Order, OrderProduct
from apps.accounts.models import UserProfile
from datetime import datetime
from crum import get_current_request

from apps.inventory.models import Product
from apps.nomenclatures.models import Manifestation


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
        # self.fields['user'].queryset = UserProfile.objects.all().filter(id=get_current_request().user.id)
        self.fields['manifestation'].queryset = Manifestation.objects.all().filter(is_active=True)
        self.fields['description'].widget.attrs['rows'] = 3

    class Meta:
        model = Order
        # fields = '__all__''
        exclude = ['start_date', 'end_date', 'created', 'updated', 'state', 'user']
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


class OrderFormAlpha(forms.ModelForm):
    products = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Order
        exclude = ['created', 'updated', 'state']

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super(OrderFormAlpha, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all().filter(id=get_current_request().user.id)
        self.fields['start_date'].label = 'Fecha de inicio'
        self.fields['end_date'].label = 'Fecha de fin'
        self.fields['user'].label = 'Usuario'
        self.fields['description'].label = 'Descripción'
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['manifestation'].label = 'Manifestación'

    def clean(self):
        cleaned_data = super().clean()
        products = cleaned_data.get('products')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        user = cleaned_data.get('user')
        description = cleaned_data.get('description')
        manifestation = cleaned_data.get('manifestation')

        # Validación de campos requeridos
        if not products:
            raise forms.ValidationError('Debe agregar al menos un producto al pedido.')
        if not start_date:
            raise forms.ValidationError('Debe ingresar una fecha de inicio.')
        if not end_date:
            raise forms.ValidationError('Debe ingresar una fecha de fin.')
        if not user:
            raise forms.ValidationError('Debe seleccionar un usuario.')
        if not manifestation:
            raise forms.ValidationError('Debe seleccionar una manifestación.')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('La fecha de inicio no puede ser mayor que la fecha de finalización.')

    def search_products(self, term, ids_exclude):
        """
            Busca productos según el término de búsqueda y los IDs de productos excluidos.

            Args:
                 term (str): Término de búsqueda.
                 ids_exclude (list): Lista de IDs de productos que se deben excluir de los resultados.

            Returns:
                list: Lista de productos que coinciden con el término de búsqueda.
        """
        products = Product.objects.filter(stock__gt=0)
        if len(term):
            products = products.filter(name__icontains=term).exclude(id__in=ids_exclude)
        data = []
        for i in products.exclude(state__exact='P')[0:10]:
            item = i.toJSON()
            item['value'] = i.__str__()
            data.append(item)
        return data

        # Lógica de procesamiento de datos

    def save(self, commit=True):
        print('SE ejecuta el save de form')
        order = super().save(commit=False)
        products = json.loads(self.cleaned_data['products'])

        if commit:
            with transaction.atomic():
                order.save()
                for i in products:
                    detail = OrderProduct()
                    detail.order_id = order.id
                    detail.product_id = int(i['id'])
                    detail.cant = int(i['cant'])
                    detail.save()

                    # Lógica para actualizar el inventario después de agregar un producto al pedido
                    detail.product.stock -= detail.cant
                    if detail.product.stock == 0:
                        detail.product.state = 'P'
                    detail.product.save()

                # Lógica para enviar una notificación al usuario
                user = Order.objects.get(pk=order.pk).user
                # notificar.send(user, destiny=user, verb='Se ha creado un pedido a su usuario exitosamente.',
                #                level='info')
                #messages.success(request, 'Se ha creado el pedido exitosamente.')


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
