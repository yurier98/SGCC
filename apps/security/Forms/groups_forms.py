from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group, Permission
from django.forms import model_to_dict


class GroupsForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=True,
        widget=FilteredSelectMultiple("Permission", is_stacked=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    # class Media:
    # css = {'all': ('/admin/css/widgets.css', '/admin/css/overrides.css'), }
    # css = {'all': ( os.path.join(BASE_DIR, 'static') '/static/admin/css/widgets.css',), }
    # js = ('/admin/jquery.js', '/admin/jsi18n/')

    class Meta:
        model = Group
        fields = 'name', 'permissions',
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre',
                    'class': 'form-control',
                }
            ),

        }

    # def toJSON(self):
    #     item = model_to_dict(self)
    #     return item

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                item = model_to_dict(instance)
                # data = instance.toJSON()
                data = item
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GroupsForm2(admin.ModelAdmin):
    filter_horizontal = ['permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = 'name', 'permissions',
        # widgets = {
        #     'name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Ingrese el nombre',
        #             'class': 'form-control',
        #         }
        #     ),
        #     'permissions': forms.SelectMultiple(attrs={
        #         'class': 'form-control select2',
        #         'style': 'width: 100%',
        #         'multiple': 'multiple'
        #     })
        #
        # }
