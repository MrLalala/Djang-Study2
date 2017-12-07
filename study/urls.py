# coding:utf-8
"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog import views as blog_views
from blog import urls as blog_urls
# from account import views as account_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', blog_views.index, name='index'),
    # 使用include注意要使用namespace,这样在使用reverse函数
    # 反向解析url时就可以直接使用
    # namespace:XXX
    # 的形式进行查找。
    url(r'^blog/', include(blog_urls, namespace='blog')),
    # url(r'^login/$', account_view.user_login, name='user_login'),
]
