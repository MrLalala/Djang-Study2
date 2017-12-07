# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post


def index(request):
    return HttpResponse('this is Index')


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': posts, })
    # return HttpResponse('this is a test')


def post_detail(request, year, month, day, post):
    # 返回一个Post类型的对象或者404 Not Found
    post = get_object_or_404(Post,
                             slug=post,
                             # status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
    # return HttpResponse('this is a test')
# Create your views here.

