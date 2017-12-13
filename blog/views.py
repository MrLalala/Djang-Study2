# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


class PostView(ListView):
    # 定义查询集
    queryset = Post.objects.all()
    # 定义对象的名字
    context_object_name = 'posts'
    # 定义每页的个数
    paginate_by = 2
    # 定义模板
    template_name = 'blog/post/list.html'


def index(request):
    return HttpResponse('this is Index')


def post_list(request, tag_slug=None):
    object_lists = Post.objects.all()

    # 添加标签过滤
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_lists = object_lists.filter(tags__in=[tag])
    # 定义分页，将posts分页，每页有三个
    paginator = Paginator(object_lists, 2)
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
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag})
    # return HttpResponse('this is a test')


def post_detail(request, year, month, day, post, posted=False):
    # 返回一个Post类型的对象或者404 Not Found
    post = get_object_or_404(Post,
                             slug=post,
                             # status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # 这里的post.comments就是来自于Comment定义外键约束时
    # 的relate_name值
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 获取表单数据
            new_comment = comment_form.save(commit=False)
            # 指定表单的post为当前post
            new_comment.post = post
            # 将该表单保存
            new_comment.save()
            # 解决了刷新页面重复提交表单的方式之一：使用HttpResponseRedirect
            # 明天研究使用crsf_token进行处理
            comment_form = CommentForm()
            posted = True
            return HttpResponseRedirect(reverse('blog:post_detail_posted', args=[
                post.publish.year,
                post.publish.strftime('%m'),
                post.publish.strftime('%d'),
                post.slug,
                True
            ]))
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'posted': posted,
                                                     'comment_form': comment_form})
    # return HttpResponse('this is a test')


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    cd = None
    error = None
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 如果验证没通过，则cleaned_data只包含通过
            # 验证的数据
            cd = form.cleaned_data
            # send Mail
            '''获取绝对路径的方式'''
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            '''配合settings设定发送者的邮箱'''
            send_mail(subject, message, '1354410847@qq.com', [cd['to']])
            '''发送成功后sent为True'''
            sent = True
        else:
            error = form.errors
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'cd': cd, 'sent': sent, 'error': error})
# Create your views here.
