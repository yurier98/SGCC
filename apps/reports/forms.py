from django import forms

from apps.inventory.models import Product, Category


class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


class ReportFilter(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    # type = forms.ChoiceField(choices=Book.BOOK_TYPES)
    state = forms.CharField(widget=forms.Select(attrs={
        'class': 'form-select',
        # 'style': 'width: 100%'
    }))
    category = forms.CharField(widget=forms.Select(attrs={
        # 'class': 'custom-select select2',
        'class': 'form-select',
        'style': 'width: 100%'
    }))
