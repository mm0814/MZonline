#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from random import Random

from common.models import EmailVerifyRecord
from django.core.mail import send_mail
from django.http import HttpResponse
from mzonline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str1 = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str1 += chars[random.randint(0, length)]
    return str1


def send_register_email(email, send_type=0):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == 0:
        email_title = "麦子在线网注册激活链接"
        email_body1 = """欢迎使用。
        请点击下面的链接激活您的账号：<br />http://localhost:8000/users/activate/%s/<br />
        (该链接在24小时内有效)<br />
        如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问""" % code

        email_body = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)
        # email_body = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/%s"%code
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:

            pass
    elif send_type == 1:
        email_title = "麦子在线网注册密码重置"
        email_body = """欢迎使用麦子学院找回密码功能。<br />
                请点击链接重置密码：<br />http://127.0.0.1:8000/reset/{0}.format(code)<br />
                (该链接在24小时内有效)<br />
                如果上面不是链接形式，请将地址复制到您的浏览器(例如IE)的地址栏再访问"""
        email_body1 = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
