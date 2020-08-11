from django.db import models
class FlowInOut15m(models.Model):
    """车站进出日客流15分钟统计数据表"""
    # '2020-06-29'
    data_dt = models.CharField(max_length=10,blank=True, null=True,verbose_name="数据产生时间")
    line_id = models.CharField(max_length=2, blank=True, null=True,verbose_name="线路编号")
    station_id = models.CharField(max_length=4, blank=True, null=True,verbose_name="车站编码")
    stat_index_cd = models.CharField(max_length=8,blank=True, null=True, verbose_name="时段索引代码")
    ticket_type = models.CharField(max_length=10,blank=True, null=True, verbose_name="票卡类型")
    ticket_sell_cnt = models.IntegerField(blank=True, null=True, verbose_name="售票客流数量")
    entry_quantity = models.IntegerField(blank=True, null=True, verbose_name="进站客流数量")
    exit_quantity = models.IntegerField(blank=True, null=True, verbose_name="出站客流数量")
    create_ts = models.DateTimeField(auto_now_add=True,verbose_name="记录创建时间")
    # 01上行 02下行
    dir = models.CharField(max_length=2,blank=True, null=True,verbose_name="方向")
    class Meta:
        db_table = 'flow_inout_15m'

class FlowTran15m(models.Model):
    """换乘站日客流15分钟统计数据表"""
    data_dt = models.CharField(max_length=10, blank=True, null=True, verbose_name='数据产生日期')
    station_id = models.CharField(max_length=4, blank=True, null=True, verbose_name="换乘车站编码")
    stat_index_cd = models.CharField(max_length=8, blank=True, null=True, verbose_name="时段索引代码")
    ticket_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="票卡类型")
    from_line_id = models.CharField(max_length=2,blank=True, null=True, verbose_name="FROM线路编码")
    # 01-上行 02-下行
    from_drct_cd = models.CharField(max_length=2, blank=True, null=True, verbose_name="进站行车方向 01-上行 02-下行")
    to_line_id = models.CharField(max_length=2,blank=True, null=True, verbose_name="TO线路编码")
    # 01-上行 02-下行
    to_drct_cd = models.CharField(max_length=2,blank=True, null=True,verbose_name="出站行车方向 01-上行 02-下行")
    quantity = models.IntegerField(blank=True, null=True,verbose_name='换乘客流数量')
    create_ts = models.DateTimeField(auto_now_add=True, verbose_name="记录创建时间")
    class Meta:
        db_table = 'flow_tran_15m'

class TrainPlan(models.Model):
    """列车计划运行数据"""
    data_dt = models.DateField(blank=True, null=True,verbose_name='数据产生日期')
    line_id = models.CharField(max_length=2, blank=True, null=True,verbose_name='线路编号')
    station_id = models.CharField(max_length=4,blank=True, null=True,verbose_name="车站编号")
    platform = models.CharField(max_length=2,blank=True, null=True,verbose_name="站台编号")
    group_code = models.CharField(max_length=10,blank=True, null=True,verbose_name="车组编号")
    global_code = models.CharField(max_length=10, blank=True, null=True,verbose_name="车次编号")
    # 1代表下行，2代表上行
    dir = models.CharField(max_length=1,blank=True, null=True,verbose_name='行驶方向')
    arrive_time = models.DateTimeField(blank=True, null=True,verbose_name='到站时间')
    depart_time = models.DateTimeField(blank=True, null=True,verbose_name='离站时间')
    dest = models.CharField(max_length=4, blank=True, null=True, verbose_name='终点站')
    ride_time = models.IntegerField(blank=True, null=True,verbose_name='乘降时间')
    up_number = models.IntegerField(blank=True, null=True,verbose_name="上车人数")
    down_number = models.IntegerField(blank=True, null=True,verbose_name='下车人数')
    arrive_load_rate = models.FloatField(blank=True, null=True,verbose_name="到站满载率")
    depart_load_rate = models.FloatField(blank=True, null=True,verbose_name='离站满载率')

    class Meta:
        db_table = 'train_plan'

class TrainReality(models.Model):
    '''列车实际运行数据表'''
    data_dt = models.DateField(blank=True, null=True, verbose_name='行车日期')
    line_id = models.CharField(max_length=2, blank=True, null=True, verbose_name='线路编号')
    station_id = models.CharField(max_length=4, blank=True, null=True, verbose_name="车站编号")
    platform = models.CharField(max_length=2, blank=True, null=True, verbose_name="站台编号")
    group_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="车组编号")
    global_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="车次编号")
    dir = models.CharField(max_length=1, blank=True, null=True, verbose_name='行驶方向')
    arrive_time = models.DateTimeField(blank=True, null=True, verbose_name='到站时间')
    depart_time = models.DateTimeField(blank=True, null=True, verbose_name='离站时间')
    dest = models.CharField(max_length=4, blank=True, null=True, verbose_name='终点站')
    ride_time = models.IntegerField(blank=True, null=True, verbose_name='乘降时间')
    up_number = models.IntegerField(blank=True, null=True, verbose_name="上车人数")
    down_number = models.IntegerField(blank=True, null=True, verbose_name='下车人数')
    arrive_load_rate = models.FloatField(blank=True, null=True, verbose_name="到站满载率")
    depart_load_rate = models.FloatField(blank=True, null=True, verbose_name='离站满载率')

    class Meta:
        db_table = 'train_reality'