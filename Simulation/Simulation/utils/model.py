from django.db import models

class BaseModel(models.Model):
    """车站基本参数基表"""
    station_id = models.CharField(max_length=4, verbose_name='车站代码')
    ps_pare_type = models.CharField(max_length=10, verbose_name='乘客参数状态类型')
    eq_id = models.CharField(max_length=20, verbose_name='设备编号')
    loc = models.CharField(max_length=20, verbose_name='设备设施位置')
    eq_status = models.CharField(max_length=10,verbose_name='设备设施状态')
    class Meta:
        abstract = True