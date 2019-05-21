from django.shortcuts import render

# Create your views here.
from .serializers import UserModelSerializer
from rest_framework.generics import CreateAPIView
from .models import User


class UserAPIView(CreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


# Create your views here.
from rest_framework.views import APIView
from luffy.libs.geetest import GeetestLib
from django.conf import settings
import random
from rest_framework.response import Response


class CaptchaAPIView(APIView):
    gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)

    """极验验证码"""

    def get(self, request):
        """提供生成验证码的配置信息"""
        user_id = '%06d' % random.randint(1, 9999)
        status = self.gt.pre_process(user_id)
        print(status)

        # 把这两段数据不要保存在session里面, 保存到redis里面
        request.session[self.gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id

        response_str = self.gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        """进行二次验证"""
        """进行二次验证"""
        print(self.gt.FN_CHALLENGE)
        print(self.gt.FN_VALIDATE)
        print(self.gt.FN_SECCODE)
        challenge = request.data.get(self.gt.FN_CHALLENGE, '')
        validate = request.data.get(self.gt.FN_VALIDATE, '')
        seccode = request.data.get(self.gt.FN_SECCODE, '')
        print(challenge)
        print(validate)
        print(seccode)

        status = request.session.get(self.gt.GT_STATUS_SESSION_KEY)

        user_id = request.session.get("user_id")
        print("status",status)
        if status:
            result = self.gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = self.gt.failback_validate(challenge, validate, seccode)

        # 返回一个随机字符串,在用户登录提供数据时一并发送到后端,进行验证
        # 后面可以使用redis保存

        print("result",result)
        return Response({"message": result})
from luffy.libs.yuntongxun.sms import CCP
from django_redis import get_redis_connection
class SMSAPIView(APIView):
    # url: users/sms/(?P<mobile>1[3-9]\d{9})
    def get(self,request,mobile):
        redis = get_redis_connection("sms_code")
        # 获取短信发送间隔
        try:
            interval = redis.get("%s_interval" % mobile)
            if interval:
                print(interval)
                return Response({"result":"-1"})
        except:
            pass

        ccp = CCP()
        sms_code = "%04d" % random.randint(1,9999)
        result = ccp.send_template_sms(mobile,[sms_code, 5],1)

        if not result:
            """发送成功"""

            redis.setex("%s_sms_code" % mobile, 5*60, sms_code)
            # 这里的值不重要,重要的是这个变量是否在redis被查找到
            redis.setex("%s_interval" % mobile, 60, 1)

        return Response({"result":result})


from .serializers import UserModelSerializer
from rest_framework.generics import CreateAPIView
from .models import User
class UserAPIView(CreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()