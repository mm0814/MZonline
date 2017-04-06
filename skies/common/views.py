#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/04/04
@author: 已开
Common模块View业务处理。
"""
from django.shortcuts import render,redirect
from django.http import HttpResponse
# from skies.common.models import UserProfile
from skies.users.views import LoginView
from skies.users.forms import  LoginForm
from django.views.generic.base import View
from django.contrib.auth import authenticate, login


# Create your views here.
# 首页

def index(request):

    return render(request, "common/index.html", locals())
def test(request):
    return render(request, "users/index.html", locals())