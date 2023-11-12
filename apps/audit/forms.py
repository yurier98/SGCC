from django import forms
from .models import Rule
from django.contrib.contenttypes.models import ContentType


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        # fields = '__all__'
        fields = ['content_type', 'check_create', 'check_edit', 'check_delete', 'is_active']

    def clean_content_type(self):

        content_type = self.cleaned_data.get('content_type')

        if self.instance and self.instance.content_type == content_type:
            return content_type

        if Rule.objects.filter(content_type=content_type).exists():
            raise forms.ValidationError('Ya existe una regla para ese objeto.')

        return content_type
