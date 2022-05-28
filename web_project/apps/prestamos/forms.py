from django.forms import ModelForm

from .models import Prestamo


class PrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        exclude = ['usuario', 'state']

        labels = {
            'fechaini': 'Fecha de inicio',
            'fechafin': 'Fecha de entrega',
            'descripcion': 'Descripcion',
            'manifestacion': 'Manifestacion',
            'maquina': 'Máquina',
            # 'usuario': 'usuario',
        }

        # widgets = {
        #     'fecha': forms.DateInput(format=('%d/%m/%Y'),
        #                              attrs={'class': 'form-control', 'placeholder': 'Selecciona la fecha',
        #                                     'type': 'date'}),
        #     'hora': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Selecciona la hora',
        #                                    'type': 'time'}),
        # 'laboratorio': forms.Select(attrs={'class': 'form-control'}),
        # 'maquina': forms.Select(attrs={'class': 'form-control'}),
        #     # 'usuario': forms.Select(attrs={'class': 'form-control'}),

        # }
        #
        # help_texts = {
        #
        #     'fecha': 'Formato de la fecha dd/mm/yyyy',
        #     'hora': 'Formato de la hora 01:50:30',
        # }
        # error_messages = {
        #     'fecha': {
        #         'max_length': ("El formato de la fecha es incorrecto ejemplo : 01/12/2020."),
        #     }
        # }
