from django.shortcuts import render

# Create your views here.
from .forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


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
