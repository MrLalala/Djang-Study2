# coding:utf-8
from django import forms
from .models import Comment


# 一个用分享帖子的邮件表单，评论不是必须的
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        # model决定了对应的表格，fields决定了要显示的input
        model = Comment
        fields = ('name', 'email', 'body')