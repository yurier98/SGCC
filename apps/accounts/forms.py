from django.forms import Form, ModelForm
from django import forms

from .models import UserProfile


class LoginForm(Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control signin-email',
                'id': 'signin-email',
                'name': 'signin-email',
                'type': 'text',
                'placeholder': 'usuario'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control signin-password',
                'id': 'signin-password',
                'name': 'signin-password',
                'type': 'password',
                'placeholder': 'contraseña'
            }
        )
    )


class ResetPasswordForm(Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su usuario',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not UserProfile.objects.filter(username=cleaned['username']).exists():
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return UserProfile.objects.get(username=username)


class ChangePasswordForm(Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = UserProfile
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'phone','solapin',  'area', \
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
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = UserProfile
        fields = 'first_name', 'last_name', 'email', 'username', 'password', 'image', 'solapin', 'phone', 'area',

        widgets = {
            # 'image': forms.FileInput(
            #     attrs={
            #         'class': 'drop-zone__input',
            #     }
            # ),
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
                    'placeholder': 'Ingrese su username',
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                                            attrs={
                                                'placeholder': 'Ingrese su password',
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

        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups',
                   'created', 'updated']

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
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
