from django.urls import path

from . import views
from django.urls import path
from .views import login_view ,login_user,ResetPasswordView, ChangePasswordView, UserUpdateProfileView
from django.contrib.auth.views import LogoutView


app_name = 'accounts'
urlpatterns = [
    #path('login/', login_view, name="login"),
    path('login/', login_user, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),
    path('update/profile/', UserUpdateProfileView.as_view(), name='user_update_profile'),

]
