#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from django import forms
from common.models import UserProfile
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required': "账号不能为空"})
    password = forms.CharField(required=True, error_messages={'required': "密码不能为空"})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required': "账号不能为空"})
    password = forms.CharField(required=True,min_length=8,max_length=50, error_messages={'required': "账号密码不能为空"})
    captcha = CaptchaField(required=True,error_messages={'required': "请输入验证码",'invalid': u'验证码错误！'})

    def clean(self):
        # 用户名
        try:
            email = self.cleaned_data['email']
        except Exception as e:
            raise forms.ValidationError(u"注册账号需为邮箱格式")
        # 验证邮箱
        user = UserProfile.objects.filter(email=email)
        if user:  # 邮箱已经被注册了
            raise forms.ValidationError(u"该账号已被注册")
        # 密码
        try:
            password = self.cleaned_data['password']
        except Exception as e:
            print 'except: ' + str(e)
            raise forms.ValidationError(u"请输入至少8位密码")

        return self.cleaned_data


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True,error_messages={'required': "请填写邮箱账号"})
    captcha = CaptchaField(error_messages={'required': "请输入验证码",'invalid': u'验证码错误！'})

    def clean(self):
        # 用户名
        try:
            email = self.cleaned_data['email']
        except Exception as e:
            raise forms.ValidationError(u"账号需为邮箱格式")
        # 验证邮箱
        # user = UserProfile.objects.get(email=email)
        # if user is None:  # 邮箱是否被注册了
        #     raise forms.ValidationError(u"该账号尚未注册")
        user = UserProfile.objects.filter(email=email)
        # if user:  # 邮箱已经被注册了
        #     raise forms.ValidationError(u"该账号已被注册")
        # try:
        #     user = UserProfile.objects.get(email=email)
        #     if user:
        #         raise forms.ValidationError(u"正在提交。。。")
        #
        #
        # except Exception:
        #     raise forms.ValidationError(u"正在提交。。。")
        return self.cleaned_data

class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6,max_length=20,error_messages={'required': "请填写账号"})
    password2 = forms.CharField(required=True, min_length=6,max_length=20,error_messages={'required': "请再次填写账号"})

    def clean(self):
        # 密码
        try:
            password1 = self.cleaned_data['password1']
        except Exception as e:
            print 'except: ' + str(e)
            raise forms.ValidationError(u"请输入至少8位密码")
        try:
            password2 = self.cleaned_data['password2']
        except Exception as e:
            print 'except: ' + str(e)
            raise forms.ValidationError(u"请输入至少8位密码")
        if password1!=password2:
            print "两次输入的密码不一致"
