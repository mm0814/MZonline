#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
create on 2017/4/4
@author:  已开
功能描述
"""

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from common.models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm

from utils.email_send import send_register_email


# Create your views here.
def index(request):
    return render(request, "users/index.html", locals())


def login1(request):
    return render(request, "users/login.html", locals())


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            print type(user_name)
            print user_name
            pass_word = request.POST.get("password", "")
            print type(pass_word)
            print pass_word
            user = authenticate(username=user_name, password=pass_word)
            # print type(user)
            # print user
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "users/index.html", {})
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活！"})
            else:
                if user != user_name :
                    msg = "用户名或密码错误"
                else:
                    msg = "登陆失败，请重试！"
                return render(request, "users/login.html", {"msg":msg})
        else:

            return render(request, "users/login.html", {"login_form":login_form})
    elif request.method == "GET":
        return render(request, "users/login.html", locals())


def register1(request):
    return render(request, "users/register.html", locals())


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return  None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/index.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "users/register.html", {"register_form": register_form, "msg": "该账户已被注册"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # send_register_email(user_name, 'register')
            send_register_email(email=user_name, send_type=0)
            return render(request, "users/login.html")
            # return  redirect('/')
        else:
            return render(request, "users/register.html", {"register_form": register_form})



class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html", locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return render(request, "common/index.html", locals())
                    return  redirect("/")
                else:
                    return render(request, "users/login.html", {"msg": "用户未激活！"})
            else:
                if user != user_name :
                    msg = "账号或密码错误，请重新输入"
                else:
                    msg = "登陆失败，请重试！"
                return render(request, "users/login.html", {"msg":msg})
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "users/forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")

            try:
                user = UserProfile.objects.get(email=email)
                send_register_email(email, 1)
                return render(request, "users/send_success.html")

            except Exception:
                return render(request,"users/register.html",{"msg":"该账号尚未注册"})


        else:
            return render(request, "users/forgetpwd.html", {"forget_form": forget_form,"msg":"找回密码申请提交失败，请重试"})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/index.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "users/login.html")

        else:
            email = request.POST.get("email", "")
            return render(request, "users/password_reset.html", {"modify_form": modify_form})
