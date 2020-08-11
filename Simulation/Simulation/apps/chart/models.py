from django.db import models
"""设备设施利用"""
class SMO_EQUFLOW(models.Model):
    """2.3.2 设备流量数据输出"""
    sceneid = models.CharField(max_length=22,verbose_name='仿真场景编号')
    equid = models.CharField(max_length=12,verbose_name='设备设施编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    equflow = models.IntegerField(verbose_name='设备设施流量')
    # 设备负荷度 = 设备流量/设备设计通行能力
    class Meta:
        db_table = 'smo_equflow'
"""
设备设施排队
楼梯入口、扶梯入口、安检机、闸机群
"""
class SMO_AREAQUEUE(models.Model):
    """2.4.7 区域排队信息统计表"""
    sceneid = models.CharField(max_length=22, verbose_name='仿真场景编号')
    equid = models.CharField(max_length=12, verbose_name='设备设施编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    quepeople = models.IntegerField(verbose_name='排队人数')
    quedensity = models.DecimalField(max_digits=5,decimal_places=2,blank=True, null=True,verbose_name='排队密度')
    class Meta:
        db_table = 'smo_areaqueue'


"""站台候车排队"""
class SMO_PEDDELAY_PED(models.Model):
    """站台候车人数统计表随时间变化"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20,verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaypeople = models.IntegerField(verbose_name='候车人数')
    class Meta:
        db_table = 'smo_peddelay_ped'

class SMO_PEDDELAY_TRA(models.Model):
    """站台候车人数统计表随列车到离站变化"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20,verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaypeople = models.IntegerField(verbose_name='候车人数')
    # 01 到站 02 离站
    trainstate = models.CharField(max_length=2,blank=True, null=True,verbose_name='列车状态')

    class Meta:
        db_table = 'smo_peddelay_tra'

class SMO_DELAYTIME_PED(models.Model):
    """2.4.4 站台候车平均时间统计表随时间变化"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20,verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaytime = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='上车人数平均候车时间')
    class Meta:
        db_table = 'smo_delaytime_ped'

class SMO_DELAYTIME_TRA(models.Model):
    """2.4.3 站台候车平均时间统计表 随列车到离站变化"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20, verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaytime = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='上车人数平均候车时间')

    class Meta:
        db_table = 'smo_delaytime_tra'

class SMO_DELAYTIMES_PED(models.Model):
    """站台平均候车次数统计表 随时间变化"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20, verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaytimes = models.IntegerField(verbose_name='上车人数平均候车时间')
    class Meta:
        db_table = 'smo_delaytimes_ped'

class SMO_DELAYTIMES_TRA(models.Model):
    """站台平均候车次数统计表 随列车到离站变化"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20, verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    delaytimes = models.IntegerField(verbose_name='上车人数平均候车时间')
    class Meta:
        db_table = 'smo_delaytimes_tra'

"""站台滞留比例"""
# 那站台候车人数 减 站台上车人数
class SMO_TRAINSERVICES(models.Model):
    """2。7.3 站台上下车人数表 每次列车到站,离站时刻插入数据"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    serid = models.CharField(max_length=20,verbose_name='上车下车类型编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    serpeople = models.IntegerField(verbose_name='上下车人数')
    class Meta:
        db_table = "smo_trainservices"


"""乘客到离站满载率"""
class SMO_ARRCAPACITY(models.Model):
    """2.7.1 列车到站满载率表"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20,verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    caprate = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='到站满载率')
    class Meta:
        db_table = 'smo_arrcapacity'

class SMO_DEPCAPACITY(models.Model):
    """2.7.2 列表离站满载率表"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20, verbose_name='上下客区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    caprate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='离站满载率')
    class Meta:
        db_table = 'smo_depcapacity'

"""乘客服务水平"""
class SMO_INTIME(models.Model):
    """2.5.1 乘客进站走行平均时间表"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20,blank=True, null=True,verbose_name='出入口编号')
    faciddis = models.CharField(max_length=20,blank=True,null=True,verbose_name='上下客区域编号（行人消失）')
    curtime = models.DateTimeField(verbose_name='当前时间')
    avgtime = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='平均进站走行时间(s)')
    class Meta:
        db_table = 'smo_intime'

class SMO_OUTTIME(models.Model):
    """2.5.2 乘客出站走行平均时间表"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    facid = models.CharField(max_length=20, blank=True, null=True, verbose_name='出入口编号')
    faciddis = models.CharField(max_length=20, blank=True, null=True, verbose_name='上下客区域编号（行人消失）')
    curtime = models.DateTimeField(verbose_name='当前时间')
    avgtime = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='平均出站走行时间(s)')

    class Meta:
        db_table = 'smo_outtime'

class SMO_TRANSFERTIME(models.Model):
    """2.5.3 乘客换乘走行平均时间表"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    tradirection = models.CharField(max_length=20, verbose_name='出入口编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    avgtime = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='平均换乘走行时间(s)')
    class Meta:
        db_table = 'smo_transfertime'




"""实时的区域速度/流量/密度"""
# class SMO_STACURDENSITY(models.Model):
#     """2.2.1 实时密度显示图数据"""
#     sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
#     areaid = models.CharField(max_length=50,verbose_name='单位区域编号')
#     curtime = models.DateTimeField(verbose_name='当前时间')
#     curdensity = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='单位区域密度')
#     class Meta:
#         db_table = "smo_stacurdensity"
#
# class SMO_STACURSPEED(models.Model):
#     """2.2.3 实时速度显示图数据"""
#     sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
#     areaid = models.CharField(max_length=50, verbose_name='单位区域编号')
#     curtime = models.DateTimeField(verbose_name='当前时间')
#     curspeed = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='单位区域速度')
#     class Meta:
#         db_table = 'smo_stacurspeed'

# class SMO_STACURFLOW(models.Model):
#     """2.2.5 实时流量显示图数据"""
#     sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
#     areaid = models.CharField(max_length=50, verbose_name='单位区域编号')
#     curtime = models.DateTimeField(verbose_name='当前时间')
#     curflow = models.IntegerField( verbose_name='单位区域流量')
#     class Meta:
#         db_table = "smo_stacurflow"
# 车站各区域乘客人数统计表
"""
注：其中要统计的区域有：站厅、站台、换乘通道、候车区域、分线路车站和整个车站

注：整个车站类型数据的的车站编号0000；
	设施序号：整个车站、站厅、站台、候车区域均为000；
			   换乘通道序号：000代表单一通道；
001代表接近车站汇总通道，002，003等代表分流通道
"""
"""车站区域客流"""
class SMO_AREAPEOPLE(models.Model):
    """2.6.4 车站各区域乘客人数实时统计表"""
    sceneid = models.CharField(max_length=30,verbose_name='仿真场景编号')
    #
    facid = models.CharField(max_length=20,verbose_name='设施编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    # 实时客流量
    areapeople = models.IntegerField(verbose_name='各区域实时人数')
    class Meta:
        db_table = 'smo_areapeople'

class SMO_AREASUMPEOPLE(models.Model):
    """2.6.5 车站各区域累计客流量统计表"""
    # 方案id
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    #
    facid = models.CharField(max_length=20, verbose_name='设施编号')
    # 时间
    curtime = models.DateTimeField(verbose_name='当前时间')
    # 累计客流量
    areasumpeople = models.IntegerField(verbose_name='各区域累计人数')
    class Meta:
        db_table = 'smo_areasumpeople'

"""累计的区域速度/流量/密度"""
class SMO_STASUMDENSITY(models.Model):
    """2.2.2 累计密度显示图数据"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    areaid = models.CharField(max_length=50, verbose_name='单位区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    sumdensity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='单位区域累计密度')

    class Meta:
        db_table = "smo_stasumdensity"

class SMO_STASUMSPEED(models.Model):
    """2.2.4 累计速度显示图数据"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    areaid = models.CharField(max_length=50, verbose_name='单位区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    sumspeed = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='单位区域累计速度')
    class Meta:
        db_table = 'smo_stasumspeed'

class SMO_STASUMFLOW(models.Model):
    """2.2.6 累计流量显示图数据"""
    sceneid = models.CharField(max_length=30, verbose_name='仿真场景编号')
    areaid = models.CharField(max_length=50, verbose_name='单位区域编号')
    curtime = models.DateTimeField(verbose_name='当前时间')
    sumflow = models.IntegerField( verbose_name='单位区域流量')
    class Meta:
        db_table = 'smo_stasumflow'






