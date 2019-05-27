# -*- coding: utf-8 -*-
# @Time    : 2019/5/15 17:35
# @Author  : Endless-cloud
# @Site    :
# @File    : serializers.py
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
from rest_framework import serializers
from .models import CourseCategory, Course


# kecheng
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ("id", "name")


# laoshi
from .models import Teacher


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "name", "title")


# from .models import CourseLesson
# class CourseLessonModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CourseLesson
#         fields = ("id","name")
#
# from .models import CourseChapter
# class CourseChapterModelSerializer(serializers.ModelSerializer):
#     coursesections = CourseLessonModelSerializer(many=True)
#     class Meta:
#         model = CourseChapter
#         fields = ["coursesections",]

class CourseModelSerializer(serializers.ModelSerializer):
    # 默认情况,序列化器转换模型数据时,默认会把外键直接转成主键ID值
    # 所以我们需要重新设置在序列化器中针对外键的序列化
    # 这种操作就是一个序列器里面调用另一个序列化器了.叫"序列化器嵌套"
    teacher = TeacherModelSerializer()

    # coursechapters = CourseChapterModelSerializer(many=True)
    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher","lesson_list","get_course_price","get_course_discount_type")


'''
课程详情
'''


class TeacherDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
        "id", "name", "title", "role", "signature", "image", "brief")


class CourseDetailModelSerializer(serializers.ModelSerializer):
    """课程详情页的序列化器"""
    teacher = TeacherDetailModelSerializer()

    class Meta:
        model = Course
        fields = (
            "id", "name", "video", "course_img", "students", "lessons", "pub_lessons", "price", "teacher",
            "course_level",
            "brief", "get_course_price", "get_course_discount_type","has_time")


from .models import CourseLesson


class CourseLessonModelSerializer(serializers.ModelSerializer):
    """课程课时"""

    class Meta:
        model = CourseLesson
        fields = ["id", "name", "duration", "free_trail", "section_link"]


from .models import CourseChapter


class CourseChapterModelSerializer(serializers.ModelSerializer):
    """课程章节"""
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ("id", "name", "coursesections", "chapter")
