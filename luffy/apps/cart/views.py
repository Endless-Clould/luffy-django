from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from courses.models import Course
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
class CartAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        """获取购物车商品课程列表"""
        # 获取当前用户ID
        user_id = 1
        # user_id = request.user.id
        # 通过用户ID获取购物车中的商品信息
        redis = get_redis_connection("cart")
        cart_goods_list = redis.hgetall("cart_%s" % user_id)  # 商品课程列表
        cart_goods_selects = redis.smembers("cart_selected_%s" % user_id)
        # redis里面的所有数据最终都是以bytes类型的字符串保存的
        print( 'selects',cart_goods_selects ) # 格式: {b'7', b'3', b'5'}
        print( 'list',cart_goods_list ) # 格式: {b'7': b'-1', b'5': b'-1'}
        # 遍历购物车中的商品课程到数据库获取课程的价格, 标题, 图片
        data_list = []
        # try:
        for course_id_bytes, expire_bytes in cart_goods_list.items():
            course_id = int(course_id_bytes.decode())
            expire = expire_bytes.decode()
            course = Course.objects.get(pk=course_id)
            data_list.append({
                "id": course_id,
                "expire": expire,
                "course_img": course.course_img.url,
                "name": course.name,
                "price": course.get_course_price(),
                "is_select": course_id_bytes in cart_goods_selects
            })
        # except:
        #     return Response(data_list, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # print(data_list)
        # 返回查询结果
        # print('dadadadad', data_list)

        return Response(data_list, status=status.HTTP_200_OK)

    """购物车视图"""
    def post(self,request):
        """购物车添加商品"""
        # 获取客户端发送过来的课程ID
        course_id = request.data.get("course_id")
        # course_id = 1
        # 验证课程ID是否有效
        try:
            Course.objects.get(pk=course_id,is_delete=False,is_show=True)
            print('course_id',course_id)
        except Course.DoesNotExist:
            return Response({"message":"当前课程不存在!"},status=status.HTTP_400_BAD_REQUEST)

        # 组装基本数据[课程ID,有效期]保存到redis
        redis = get_redis_connection("cart")
        # user_id = 1
        user_id = request.user.id
        # transation: 事务
        # 作用: 可以设置多个数据库操作看成一个整体,这个整理里面每一条数据库操作都成功了,事务才算成功,
        #      如果出现其中任意一个数据库操作失败,则整体一起失败!
        # 事务可以提供 提交事务 和 回滚事务 的功能
        # 不仅mysql中存在事务,在redis中也有事务的概念,但是叫"管道 pipeline"
        try:
            # 创建事务[管道]对象
            pipeline = redis.pipeline()
            # 开启事务
            pipeline.multi()
            # 添加一个成员到指定名称的hash数据中[如果对应名称的hash数据不存在,则自动创建]
            # hset(名称,键,值)
            pipeline.hset("cart_%s" % user_id, course_id, -1) # -1表示购买的课程永久有效

            # 添加一个成员到制定名称的set数据中[如果对应名称的set数据不存在,则自动创建]
            # sadd(名称,成员)
            pipeline.sadd("cart_selected_%s" % user_id, course_id )

            # 提交事务[如果不提交,则事务会自动回滚]
            pipeline.execute()

        except:
            return Response({"message": "添加课程到购物车失败!请联系客服人员~"},status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 返回结果,返回购物车中的商品数量
        count = redis.hlen("cart_%s" % user_id)

        return Response({
            "message": "成功添加课程到购物车!",
            "count": count,
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """购物车更新商品信息"""
        # 获取当前登录用户ID
        # user_id = request.user.id
        user_id = 1

        # 接受课程ID,判断课程ID是否存在
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(pk=course_id, is_delete=False, is_show=True)
        except Course.DoesNotExist:
            return Response({"message": "当前课程不存在!"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取勾选状态
        is_select = request.data.get("is_select")
        print('is_select',is_select,type(is_select))
        # print('false')


        # 链接redis
        redis = get_redis_connection("cart")

        # 修改购物车中指定商品课程的信息
        if is_select=='true':
            # 从勾选集合中新增一个课程ID
            redis.sadd("cart_selected_%s" % user_id, course_id)
            print('课程select增加成功')
        else:
            redis.srem("cart_selected_%s" % user_id, course_id)
            print('课程select删除成功')

        return Response({
            "message": "修改购物车信息成功!"
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        """更新购物城中的商品信息"""
        # 获取当前登录的用户ID
        # user_id = 1
        user_id = request.user.id

        # 获取当前操作的课程ID
        course_id = request.data.get("course_id")

        # 获取新的有效期
        expire = request.data.get("expire")

        # 获取redis链接
        redis = get_redis_connection("cart")

        # 更新购物中商品课程的有效期
        redis.hset("cart_%s" % user_id, course_id, expire)

        return Response({
            "message": "修改购物车信息成功!"
        }, status=status.HTTP_200_OK)