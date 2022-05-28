from django.contrib import auth
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import LoginForm


# Create your views here.
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    # Correct password, and the user is marked "active"
                    auth.login(request, user)
                    # Redirect to a success page.
                    return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'autentications/login.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "autentications/login.html", {"form": form, "msg": msg})

def logout_user(request):
    auth.logout(request)
    return redirect('loguiar_usuario')
