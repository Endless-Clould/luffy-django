# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 16:58
# @Author  : Endless-cloud
# @Site    : 
# @File    : adminx.py
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
import xadmin

from .models import CourseCategory


class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)

from .models import Course


class CourseModelAdmin(object):
    """课程模型管理类"""
    pass


xadmin.site.register(Course, CourseModelAdmin)

from .models import Teacher


class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)

from .models import CourseChapter


class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)

from .models import CourseLesson


class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)

from .models import PriceDiscountType


class PriceDiscountTypeModelAdmin(object):
    """优惠类型模型管理类"""
    pass


xadmin.site.register(PriceDiscountType, PriceDiscountTypeModelAdmin)

from .models import PriceDiscount


class PriceDiscountModelAdmin(object):
    """价格优惠策略模型管理类"""
    pass


xadmin.site.register(PriceDiscount, PriceDiscountModelAdmin)

from .models import CoursePriceDiscount


class CoursePriceDiscountModelAdmin(object):
    """课程与价格优惠关系模型管理类"""
    pass


xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)

from .models import CourseTime


class CourseTimeModelAdmin(object):
    """课程与价格优惠关系模型管理类"""
    list_display = ["course", "title", "timer", "price"]


xadmin.site.register(CourseTime, CourseTimeModelAdmin)
