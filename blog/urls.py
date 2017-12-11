# coding:utf-8
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    # url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.PostView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail, name='post_detail'),
]