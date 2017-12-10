# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return HttpResponse('this is Index')


def post_list(request):
    object_lists = Post.objects.all()
    # 定义分页，将posts分页，每页有三个
    paginator = Paginator(object_lists, 3)
    # 获取当前页数
    page = request.GET.get('page')
    try:
        # 获取要显示的那一页
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 不足一页，就显示第一页
        # 当第一次get时使用的也是这个方法。
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超过总页数则返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page':page})
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

