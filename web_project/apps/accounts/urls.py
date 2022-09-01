from django.urls import path

from . import views
from django.urls import path
from .views import *

#app_name = 'accounts'

urlpatterns = [
    # path('login/', login_view, name="login"),
    #path('login/', login_user, name="login"),
    path('login/', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),

     # path('choose/profile/<int:pk>/', UserChooseGroup.as_view(), name='user_choose_profile'),

    # las url para las vistas deL CRUD de Usuario debe estar contenidas dentro del modulo de admin

    path('profile/update/', UserUpdateProfileView.as_view(), name='user_update_profile'),
    path('profile/details/', UserDetailProfileView.as_view(), name='user_details_profile'),
    path('change/password/', UserChangePasswordView.as_view(), name='user_change_password'),



]
