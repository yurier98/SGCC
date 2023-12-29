from django.contrib.auth import authenticate
from django.forms import Form
from django import forms
from widget_tweaks.templatetags.widget_tweaks import render_field, add_class
from apps.accounts.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', required=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control ',
                                   'placeholder': 'Ingrese su usuario',
                                   'autocomplete': 'off',
                               }))
    password = forms.CharField(label='Contraseña', required=False,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control ',
                                   'placeholder': 'Ingrese la contraseña',
                                   'type': 'password',
                                   'autocomplete': 'off',
                               }))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    # clean validation
    def clean(self):
        cleaned_data = super().clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username:
            self.add_error('username', 'Por favor ingrese un nombre de usuario.')
            self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})

        if not password:
            self.add_error('password', 'Por favor ingrese la contraseña.')
            self.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})

        # if not username:
        #     self._errors['username'] = self.error_class([
        #         'Por favor ingrese un nombre de usuario.'])
        #     self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})

        # if not password:
        #     self._errors['password'] = self.error_class([
        #         'Por favor ingrese la contraseña.'])
        #     self.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})

        return cleaned_data


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
