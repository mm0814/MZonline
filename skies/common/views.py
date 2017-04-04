#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2017/04/04
@author: 已开
Common模块View业务处理。
"""
from django.shortcuts import render

# Create your views here.
# 首页
def index(request):
    return render(request, "common/index.html", locals())
