#!/usr/bin/env python
# _*_ coding:utf-8 _*_


"""mzonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from common.views import *
from skies.users.views import  ActiveUserView,ResetView,ModifyPwdView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('common.urls')),
    url(r'^course/', include('course.urls')),
    url(r'^users/', include('users.urls')),
    # url(r'^test/$',test,name='test'),
    # 激活用户
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 重置密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    # url(r'^modify_pwd/$',ModifyPwdView.as_view(),name="modify_pwd"),
]
