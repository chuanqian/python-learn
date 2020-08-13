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
