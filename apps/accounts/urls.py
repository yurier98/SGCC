from django.urls import path

from . import views
from django.urls import path
from .views import *

#app_name = 'accounts'

urlpatterns = [

    #################  Usuarios   #####################################
    path('users', UserListView.as_view(), name='user_list'),
    path('user/add', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),


    path('user/desactivate/<int:pk>/', views.UserDeactivateView.as_view(), name='user_desactivate'),
    path('user/activate/<int:pk>/', views.UserDeactivateView.as_view(), name='user_activate'),


     # path('choose/profile/<int:pk>/', UserChooseGroup.as_view(), name='user_choose_profile'),

    # las url para las vistas deL CRUD de Usuario debe estar contenidas dentro del modulo de admin

    path('profile/update/', UserUpdateProfileView.as_view(), name='profile_update'),
    path('profile/details/', UserDetailProfileView.as_view(), name='profile_details'),
    # path('change/password/', UserChangePasswordView.as_view(), name='user_change_password'),



]
