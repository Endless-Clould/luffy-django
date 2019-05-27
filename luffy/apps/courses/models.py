from django.db import models
from luffy.utils.models import BaseModel
from datetime import datetime
from decimal import Decimal


# Create your models here.
class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name


from ckeditor_uploader.fields import RichTextUploadingField


class Course(BaseModel):
    """
    专题课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    video = models.FileField(upload_to="video", null=True, blank=True, default=None, verbose_name="封面视频")
    brief = RichTextUploadingField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name

    def get_course_discount_type(self):
        now = datetime.now()
        try:
            course_prices = self.prices.get(start_time__lte=now, end_time__gte=now, is_delete=False, is_show=True)
            # 获取优惠活动类型
            return course_prices.discount.discount_type.name
        except:
            return ""

    def get_course_price(self,price=0):
        # 获取当前课程的真实价格
        # 获取当前课程的价格策略
        self.price = price if price != 0 else self.price  # 判断调用当前方法时,是否定义了价格
        now = datetime.now()
        try:
            course_prices = self.prices.get(start_time__lte=now, end_time__gte=now, is_delete=False, is_show=True)

            # 价格优惠条件判断,原价大于优惠条件才参与活动
            if self.price < course_prices.discount.condition:
                return self.price

            # 当优惠公式为多行文本,则表示满减
            if course_prices.discount.sale[0] == "满":
                sale_list = course_prices.discount.sale.split("\r\n")
                sale_price_list = []
                # 通过遍历提取所有策略项的优惠价格值
                for sale_item in sale_list:
                    sale = int(sale_item[1: sale_item.index("-")])
                    sele_price = int(sale_item[sale_item.index("-") + 1:])
                    if self.price >= sale:
                        sale_price_list.append(sele_price)

                # 当前课程只能享受一个最大优惠
                return self.price - max(sale_price_list)

            # 当优惠公式为-1,则表示真实价格为0
            if course_prices.discount.sale == "-1":
                return 0

            # 当优惠公式为*开头,则表示折扣
            if course_prices.discount.sale[0] == "*":
                sale = Decimal(course_prices.discount.sale[1:])
                return self.price * sale

            # 当优惠公式为负数,则表示减免
            if course_prices.discount.sale[0] == "-":
                sale = Decimal(course_prices.discount.sale[1:])
                real_price = self.price - sale
                return real_price if real_price > 0 else 0

        except:
            print("---没有优惠---")

        return self.price

    def lesson_list(self):
        """获取当前课程的前8个课时展示到列表中"""

        # 获取所有章节
        chapters_list = self.coursechapters.filter(is_delete=False, is_show=True)
        lesson_list = []
        if chapters_list:
            for chapter in chapters_list:
                lessons = chapter.coursesections.filter(is_delete=False, is_show=True)[:4]
                if lessons:
                    for lesson in lessons:
                        lesson_list.append({
                            "id": lesson.id,
                            "name": lesson.name,
                            "free_trail": lesson.free_trail
                        })

        return lesson_list[:4]

    def course_level(self):
        """把课程难度数值转换成文本"""
        return self.level_choices[self.level][1]







    def has_time(self):
        """计算活动的剩余时间"""
        now = datetime.now()
        try:
            course_prices = self.prices.get(start_time__lte=now, end_time__gte=now, is_delete=False, is_show=True)
            # 把 活动结束时间 - 当前时间 = 剩余时间
            return int(course_prices.end_time.timestamp() - now.timestamp())
        except:
            print("---活动过期了----")

        return 0






class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, blank=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


"""价格相关的模型"""


class PriceDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_price_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = "课程优惠类型"

    def __str__(self):
        return "%s" % (self.name)


class PriceDiscount(BaseModel):
    """课程优惠模型"""
    discount_type = models.ForeignKey("PriceDiscountType", on_delete=models.CASCADE, related_name='pricediscounts',
                                      verbose_name="优惠类型")
    discount_name = models.CharField(max_length=150, verbose_name="优惠活动名称")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件")  # 就是最少多少钱.
    sale = models.TextField(verbose_name="优惠公式", help_text="""
    -1表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    $号开头表示积分兑换，例如$50表示可以兑换50积分<br>
    表示满减,则需要使用 原价-优惠价格,例如表示,课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-20<br>

    """)

    class Meta:
        db_table = "ly_price_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s,优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)


class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="prices", verbose_name="课程")
    discount = models.ForeignKey("PriceDiscount", on_delete=models.CASCADE, related_name="courses", verbose_name="优惠活动")
    start_time = models.DateTimeField(verbose_name="优惠策略的开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略的结束时间")

    class Meta:
        db_table = "ly_course_price_dicount"
        verbose_name = "课程与优惠策略的关系表"
        verbose_name_plural = "课程与优惠策略的关系表"

    def __str__(self):
        return "优惠: %s,开始时间:%s,结束时间:%s" % (self.discount.discount_name, self.start_time, self.end_time)









"""课程有效期"""
class CourseTime(BaseModel):
    """课程有效期表"""
    timer = models.IntegerField(verbose_name="购买周期",default=30,help_text="单位:天<br>建议按月书写,例如:1个月,则为30.")
    title = models.CharField(max_length=150, null=True, blank=True, verbose_name="购买周期的文本提示", default="1个月有效", help_text="要根据上面的购买周期,<br>声明对应的提示内容,<br>展示在购物车商品列表中")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="coursetimes", verbose_name="课程")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)

    class Meta:
        db_table = "ly_course_time"
        verbose_name = "课程有效期表"
        verbose_name_plural = "课程有效期表"

    def __str__(self):
        return "课程:%s,周期:%s,价格:%s" % (self.course, self.timer, self.price)