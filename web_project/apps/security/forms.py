from django import forms
from django.contrib.auth.models import User, Group


class GroupsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = 'name',  'permissions',
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                    'class': 'form-control',
                }
            ),
            'permissions': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            })

        }
