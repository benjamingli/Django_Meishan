# coding=utf8
from django import forms
from django.core.exceptions import ValidationError

from .models import Account

def validate_username_exist(value):
    if Account.objects.filter(username=value).count() == 0:
        raise ValidationError(
            '用户名%(value)s不存在',
            params={'value': value},
        )

class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户',
        widget=forms.TextInput(attrs={
            'placeholder': '用户名',
            }),
        min_length=2,
        max_length=20,
        validators=[validate_username_exist],
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名长度为2-20字符',
            'max_length': '用户名长度为2-20字符',
        })
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'placeholder': '密码',
            }),
        min_length=4,
        max_length=20,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码长度为4-20字符',
            'max_length': '密码长度为4-20字符',
        })
