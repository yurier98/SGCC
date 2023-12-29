from django import forms
from .models import ReportDefinition


class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportDefinition
        fields = ['report_type', ]

    def clean_report_type(self):
        report_type = self.cleaned_data.get('report_type')

        if ReportDefinition.objects.filter(report_type=report_type).exists():
            raise forms.ValidationError('Ya existe un report_type con este nombre.')

        return report_type
