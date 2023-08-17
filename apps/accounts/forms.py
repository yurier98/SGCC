from django.forms import Form, ModelForm
from django import forms

from .models import UserProfile


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = UserProfile
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'phone', 'solapin', 'area', \
            'groups', 'image', 'is_active', 'is_superuser'

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                    'class': 'form-control',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                    'class': 'form-control',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su usuario',
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                                            attrs={
                                                'placeholder': 'Ingrese su contraseña',
                                                'class': 'form-control',
                                            }
                                            ),
            'solapin': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Solapín',
                    'class': 'form-control',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su teléfono',
                    'class': 'form-control',
                }
            ),
            'area': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su área',
                    'class': 'form-control',
                }
            ),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_staff', 'created', 'updated']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = UserProfile.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = 'image', 'phone'

        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su teléfono',
                    'class': 'form-control',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups',
                   'created', 'updated']
