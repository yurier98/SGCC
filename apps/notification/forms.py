from django import forms
from .models import EmailNotification


class EmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['rows'] = 3

    class Meta:
        model = EmailNotification
        fields = ['email_to', 'subject', 'body']
        widgets = {
            'email_to': forms.TextInput(attrs={
                'placeholder': 'Dirección email',
                'class': 'form-control',
                'readonly': True
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Asunto',
                'class': 'form-control',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Escribe algo ... ',
                'class': 'form-control',
                'style': 'height: 100px',
                'rows': 3,
                'cols': 3
            }),
        }
