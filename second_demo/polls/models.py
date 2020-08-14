from django.db import models


# Create your models here.
class Subject(models.Model):
    no = models.AutoField(primary_key=True, verbose_name="唯一标识，编号", blank=True)
    name = models.CharField(max_length=50, verbose_name="名称")
    intro = models.CharField(max_length=1000, verbose_name="介绍")
    is_host = models.BooleanField(default=True, verbose_name="是否热门")

    class Meta:
        managed = False
        db_table = "tb_subject"
        verbose_name = "学科"
        verbose_name_plural = "学科"


class Teacher(models.Model):
    no = models.AutoField(primary_key=True, verbose_name="老师编号")
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.BooleanField(default=True, verbose_name="性别")
    birth = models.DateTimeField(null=True, verbose_name="生日")
    intro = models.CharField(max_length=1000, verbose_name="自我介绍")
    photo = models.ImageField(max_length=255, verbose_name="照片")
    good_count = models.IntegerField(default=0, db_column="goodcount", verbose_name="好评数")
    bad_count = models.IntegerField(default=0, db_column="badcount", verbose_name="差评数")
    subject = models.ForeignKey(Subject, models.DO_NOTHING, db_column="sno")

    class Meta:
        managed = False
        db_table = "tb_teacher"
        verbose_name = "学科老师信息"
        verbose_name_plural = "学科老师信息"


class User(models.Model):
    no = models.AutoField(verbose_name="编号", primary_key=True)
    username = models.CharField(max_length=30, verbose_name="用户名")
    password = models.CharField(max_length=50, verbose_name="密码")
    tel = models.CharField(max_length=12, verbose_name="电话号码")
    reg_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_visit = models.DateTimeField(null=True, verbose_name="最后访问时间")

    class Meta:
        db_table = "tb_user"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期', null=True)
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)

    class Meta:
        db_table = "tb_book_info"
        verbose_name = "图书信息"
        verbose_name_plural = "图书信息"


# 定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )
    hname = models.CharField(max_length=20, verbose_name='名称')
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    hcomment = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    hbook = models.ForeignKey(BookInfo, related_name='heroes', on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname


class BookIntro(models.Model):
    book_id = models.AutoField(primary_key=True, verbose_name="图书编号")
    book_name = models.CharField(max_length=100, verbose_name="图书名称")

    class Meta:
        db_table = "tb_book_intro"
        verbose_name = "图书"
        verbose_name_plural = "图书信息表"
