# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishManager(models.Manager):
    # 获取结果集的方法
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # @staticmethod
    def get_absolute_url(self):
        # 关于第一个参数：就是urls.py中定义的views.py名。
        # 如果是使用了include选项的url，需要给include指定命名空间
        # 使用namespace:name的方式进行引用。
        # 注意：这是通过url进行查找的。
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug, ])

# Create your models here.
