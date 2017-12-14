# coding:utf-8
from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


# 通过装饰器拿到所有已经发布的帖子的数量
# 通过simple_tag装饰后的方法就可以当作标签用了！
# 如果想指定标签的名字，可以使用
# register.simple_tag(name="my name")
@register.simple_tag
def total_posts():
    return Post.objects.count()


# 通过装饰器可以直接引入templates,所有使用
# 该标签的都会直接调用
# inclusion_tag中定义的模板
# 关于自定义标签中的参数，要在模板中指定，同时最好加入默认值
# 获取最新发布的5篇贴子
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 获取评论前count的帖子
# assignment_tag标签会将返回值包含在一个变量中
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(count_num=Count('comments'))\
        .order_by('-count_num')[:count]


@register.simple_tag
def test():
    return 'this is a test for filter, test test test'


@register.simple_tag
def phone():
    return 17864215631
