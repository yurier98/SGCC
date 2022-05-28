from django.contrib import admin

from .models import Perfil


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'solapin', 'categoria']
    #list_filter = ['is_superuser']
    #search_fields = ['username', 'first_name', 'last_name']


admin.site.register(Perfil, ProfileAdmin)
