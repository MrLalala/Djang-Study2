# coding:utf-8
from django.utils.safestring import mark_safe
from django import template
from django.template.defaultfilters import stringfilter
import markdown


register = template.Library()


@register.filter(need_autoescape=True)
@stringfilter
def number(text, autoescape=True):
    format_text = text[:3] + '****' + text[7: ]
    return mark_safe(format_text)


# 依靠name选项指定在使用时的过滤器名称
# 注意过滤器使用参数的方式，第一个参数就是|前边的
# 第二个参数需要使用 : 在后边进行传递
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


# 如果不指定filter后边的name，那么
# 过滤器的名字就是定义的函数名
@register.filter
def cut(text, arg1):
    return text.replace(arg1, 'filter')


# 第二种自定义过滤器的注册方法
# 通过stringfilter将参数包装成str类型
@register.filter(is_safe=True)
@stringfilter
def lower(text):
    return text.lower()


# 将电话号中间四位转为****