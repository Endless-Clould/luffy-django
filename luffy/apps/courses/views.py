from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework.generics import ListAPIView
from .models import CourseCategory, Course
from .serializers import CourseCategoryModelSerializer


class CourseCategoryAPIView(ListAPIView):
    """课程分类列表"""
    queryset = CourseCategory.objects.filter(is_delete=False, is_show=True).order_by("-orders")
    serializer_class = CourseCategoryModelSerializer


from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """自定义分页器"""
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_size = 3


from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class CourseAPIView(ListAPIView):
    """课程列表信息"""
    queryset = Course.objects.filter(is_delete=False, is_show=True).order_by("orders")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields = ('id', 'students', 'price')
    pagination_class = StandardPageNumberPagination


# 课程详细
from rest_framework.generics import RetrieveAPIView
from .serializers import CourseDetailModelSerializer


class CourseDeitalAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_delete=False, is_show=True).order_by("orders")
    serializer_class = CourseDetailModelSerializer




from rest_framework.generics import ListAPIView
from .serializers import CourseChapterModelSerializer
from .models import CourseChapter
class CourseChapterAPIView(ListAPIView):
    """课程章节信息"""
    queryset = CourseChapter.objects.filter(is_delete=False, is_show=True).order_by("orders")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']




'''
生成播放器视频
'''
from rest_framework.views import APIView
from luffy.libs.polyv import PolyvPlayer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
class PolyvAPIView(APIView):
    """生成播放视频的playsafetoken"""
    """播放页面的当前访问者只能是用户,不能是游客"""
    # permission_classes = (IsAuthenticated,)
    def get(self,request):
        # 获取客户端要播放的视频vid
        vid = request.query_params.get("vid")
        # 获取客户端的IP地址
        remote_addr = request.META.get("REMOTE_ADDR")
        # 获取用户的ID和用户名[测试]
        user_id = request.user.id
        user_name = request.user.username

        # 生成token
        polyv = PolyvPlayer()
        data = polyv.get_video_token(vid, remote_addr,user_id, user_name)
        print(data)

        return Response(data["token"])