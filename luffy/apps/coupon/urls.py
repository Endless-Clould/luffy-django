# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 16:27
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
from django.urls import path
from . import views
urlpatterns = [
    path(r"list/",views.UserCouponAPIVew.as_view()),
]