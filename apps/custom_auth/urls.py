# from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginFormView, LogoutView, ResetPasswordView, ChangePasswordView, login_view

urlpatterns = [
    # path('', views.HomePage.as_view(), name='home'),

    # path('', LoginFormView.as_view(), name="login"),
    # path('login/', LoginView.as_view(), name='login'),

    path('login/', LoginFormView.as_view(), name='login'),
    # path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_password'),

]
