from django import forms


class LoginForm(forms.Form):

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