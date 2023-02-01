from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login

User = get_user_model()


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username_ = form.cleaned_data["username"]
            user_obj = User.objects.get(username__iexact=username_)
            login(request, user_obj)
            return HttpResponseRedirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect('/accounts/login')
