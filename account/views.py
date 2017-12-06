# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm


def user_login(request):
    # 定义错误信息
    error = ''
    # 当提交时
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # 验证数据是否合理
        if form.is_valid():
            # 获得form数据
            cd = form.cleaned_data
            # 当存在该用户时
            if User.objects.filter(username=cd['username']):
                # 验证
                user = authenticate(username=cd['username'],
                                    password=cd['password'])
                # 查看是否通过
                if user is not None:
                    # 如果是active状态
                    if user.is_active:
                        # 将该用户加入session中
                        login(request, user)
                        # 返回验证通过信息
                        return HttpResponse('Authenticated successfully')
                    # 非active状态，返回错误信息
                    else:
                        error = 'Disabled account'
                # 非通过状态
                else:
                    error = 'Password is Error'
            # 查询不到用户
            else:
                error = 'User Not Found'
        # 数据不合理
        else:
            error = "Invalid login"
    # request是get
    else:
        form = LoginForm()
    # 返回login页面，包括form和错误信息
    return render(request, 'account/login.html', {'form': form, 'error':error})
# Create your views here.
