# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


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
    tags = TaggableManager()

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


class Comment(models.Model):
    # relate_name是给这个属性命名，这样就可以通过这个名反向定义到
    # 这个对象。如，可以使用comment.post获取到帖子，
    # 通过post.comments.all()来获取这篇帖子相关的评论。
    # 如果不定义relate_name，那么系统默认会使用[模型名]_set来命名，
    # 在本例中，就要使用post.comment_set.all()来读取帖子相关的评论
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)
# Create your models here.
