from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework.generics import ListAPIView

from home.serializers import BannerInfoSerializer
from .models import BannerInfo


#
class BannerInfoListAPIView(ListAPIView):
    """
    轮播图列表
    """
    queryset = BannerInfo.objects.filter(Q(is_show=True) & Q(is_delete=False)).order_by("-orders")
    # 商家上架并且没有逻辑删除的queryset 倒叙展示出来.
    serializer_class = BannerInfoSerializer


from .models import NavInfo
from .serializers import NavInfoSerializer


class NavInfoAPIView(ListAPIView):
    """
    导航列表
    """
    queryset = NavInfo.objects.filter(Q(is_show=True) & Q(is_delete=False) & Q(opt=0)).order_by("-orders")
    serializer_class = NavInfoSerializer
