# -*- coding: utf-8 -*-
# @Time    : 2019/5/12 15:05
# @Author  : Endless-cloud
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
'''
 　　　　　　　 ┏┓　 ┏┓+ +
 　　　　　　　┏┛┻━━━┛┻┓ + +
 　　　　　　　┃　　　　　　┃ 　
 　　　　　　　┃　　　━　　 ┃ ++ + + +
 　　　　　　 ████━████  ┃+
 　　　　　　　┃　　　　　　　┃ +
 　　　　　　　┃　　　┻　　　┃
 　　　　　　　┃　　　　　　┃ + +
 　　　　　　　┗━┓　　　┏━┛
 　　　　　　　　 ┃　　　┃　　　　　　　　　　　
 　　　　　　　　 ┃　　　┃ + + + +
 　　　　　　　　 ┃　　　┃　　　　Code is far away from bug with the animal protecting　　　　　　　
 　　　　　　　　 ┃　　　┃ + 　　　　神兽保佑,代码无bug　　
 　　　　　　　　 ┃　　　┃
 　　　　　　　　 ┃　　　┃　　+　　　　　　　　　
 　　　　　　　　 ┃　 　 ┗━━━┓ + +
 　　　　　　　　 ┃ 　　　　   ┣┓
 　　　　　　　　 ┃ 　　　　　 ┏┛
 　　　　　　　　 ┗┓┓┏━┳┓┏┛ + + + +
 　　　　　　　　  ┃┫┫ ┃┫┫
 　　　　　　　　  ┗┻┛ ┗┻┛+ + + +
 '''
from django.urls.conf import path
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path(r'login/', obtain_jwt_token, name='login'),
]