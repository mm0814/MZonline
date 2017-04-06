#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
create on 2017/4/4
@author:  已开
功能描述
"""
from django.conf.urls import include,url
from django.contrib import admin
from users import views
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView


urlpatterns = [

    url(r'^index/$',views.index),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    # url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),

    url(r'^forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # url(r'^login1/$',views.login1),
    # url(r'^register1/$', views.register1),
    # url(r'^user_login/$',views.user_login),



]
