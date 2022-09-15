from django.contrib import admin

from .models import UserProfile


class PerfileAdmin(admin.ModelAdmin):
    search_fields = ('username'),
    ordering = ['username']
    list_filter = ('area',)

    # filter_horizontal = 'groups', 'permissions', 'any_other_m2m_field'
    # filter_horizontal = 'groups'
    filter_horizontal = ['groups', 'user_permissions']

    list_display = [
        "username",
        "area",
        "ocupacion",
        "phone",
        "is_active",
        "grupos",
    ]

    def grupos(self, obj):
        return "\n".join([g.name for g in obj.groups.all()])


admin.site.register(UserProfile, PerfileAdmin)
# admin.site.register(Menu)


# class LoginAndPassManagerVarsConfigAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "account_logout_url",
#         "account_pasword_change_redirect_url",
#         "password_regex",
#         "store_password_history",
#         "password_history_life",
#         "password_expiry_time",
#         "block_auth_from_other_ip",
#         "faillogin_attemps_before_deactive",
#         "token_validity_duration",
#     ]
#     fields = [
#         "account_logout_url",
#         "account_pasword_change_redirect_url",
#         "password_regex",
#         "store_password_history",
#         "password_history_life",
#         "password_expiry_time",
#         "block_auth_from_other_ip",
#         "faillogin_attemps_before_deactive",
#         "token_validity_duration",
#     ]
# admin.site.register(LoginAndPassManagerVarsConfigAdmin)
