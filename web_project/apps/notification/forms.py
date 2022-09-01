from django import forms


class EmailForm(forms.Form):
    email_to = forms.EmailField(label='To')
    title = forms.CharField(max_length=140)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = ('email_to', 'title', 'message')


class NotificationFilterForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
