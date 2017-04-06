#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
create on 2017/4/4
@author:  已开
功能描述
"""

from django.conf.urls import url
from django.contrib import admin
from common import views

urlpatterns = [

    url(r'^$', views.index, name='index'),


]
