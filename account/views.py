# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm


def user_login(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']):
                user = authenticate(username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponse('Authenticated successfully')
                    else:
                        error = 'Disabled account'
                else:
                    error = 'Password is Error'
            else:
                error = 'User Not Found'
        else:
            error = "Invalid login"
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'error':error})
# Create your views here.
