from django.db import models


class TrainLine(models.Model):
    """线路表"""
    line_id = models.CharField(max_length=2, primary_key=True, verbose_name="线路编号")
    line_name = models.CharField(max_length=10, blank=True, null=True, verbose_name="线路名称")

    class Meta:
        db_table = 'train_line'

    @property
    def station_list(self):
        """获取某条线路所有的车站"""
        station_list = []
        for station in self.stations.all():
            station_list.append({
                'station_id': station.station_id,  # 车站编码  唯一的
                'station_name': station.station_name,  # 车站名称
            })
        return station_list

class TrainStation(models.Model):
    """地铁车站表"""
    station_id = models.CharField(max_length=4, primary_key=True, verbose_name="车站编号")
    # 展示
    line = models.ForeignKey("TrainLine", related_name='stations', on_delete=models.CASCADE, db_constraint=False,verbose_name="线路编号")
    station_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="车站名称")
    # 展示
    des = models.TextField(max_length=150, blank=True, null=True, verbose_name="车站描述")
    station_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="车站类型")
    pf_type = models.CharField(max_length=30, blank=True, null=True, verbose_name="站台类型")
    passages_num = models.IntegerField(blank=True, null=True, verbose_name="出入口数")
    station_pic = models.ImageField(upload_to='station', max_length=255, blank=True, null=True, verbose_name="车站图片路径")
    current_image_name = models.CharField(max_length=15, blank=True, null=True, verbose_name="当前车站图片名称")
    wo_peak_hours = models.CharField(max_length=30, blank=True, null=True, verbose_name="工作日高峰时段")
    ho_peak_hours = models.CharField(max_length=30, blank=True, null=True, verbose_name="节假日高峰时段")
    current_model_version = models.CharField(max_length=10, blank=True, null=True, verbose_name="当前版本")
    model_version_create_time = models.CharField(max_length=20, blank=True, null=True, verbose_name="模型版本的上传时间")

    class Meta:
        db_table = "train_station"

    @property
    def sim_station_name(self):
        sim_station_name = self.line.line_name + self.station_name
        return sim_station_name

class ModelVersion(models.Model):
    """车站模型版本表"""
    version_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="版本号")
    founder = models.CharField(max_length=20, blank=True, null=True, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 这个字段需要更新
    model_url = models.FileField(upload_to='static/model', null=True, verbose_name="车站模型路径")
    version_des = models.TextField(max_length=200, null=True, blank=True, verbose_name="版本描述")
    station = models.ForeignKey('TrainStation', related_name='model_versions', db_constraint=False,
                                on_delete=models.CASCADE, verbose_name="车站仿真模型版本")
    class Meta:
        db_table = "model_version"

    @property
    def current_model_version(self):
        return self.station.current_model_version

class StationImage(models.Model):
    """车站图纸表"""
    image_name = models.CharField(max_length=10, null=True, blank=True, verbose_name="图纸名称")
    image_format = models.CharField(max_length=10, null=True, blank=True, verbose_name="图片格式")
    image_url = models.ImageField(upload_to='station', null=True, verbose_name="车站图片路径")
    founder = models.CharField(max_length=20, blank=True, null=True, verbose_name="创建人")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    station = models.ForeignKey('TrainStation', related_name='station_images', db_constraint=False,on_delete=models.CASCADE, verbose_name="车站图纸")

    class Meta:
        db_table = 'station_image'

    @property
    def current_image_name(self):
        return self.station.current_image_name

class TrainScheme(models.Model):
    """仿真方案表"""
    # 第一页的参数
    scheme_id = models.CharField(primary_key=True, max_length=50, verbose_name="仿真方案id")
    station_id = models.CharField(max_length=4, blank=True, null=True, verbose_name="车站编码")
    station_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="仿真车站名称")
    scheme_type = models.CharField(max_length=4, blank=True, null=True, verbose_name="仿真方案类型")
    scheme_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="方案名称")
    creater = models.CharField(max_length=50, blank=True, null=True, verbose_name="创建人")
    create_time = models.DateTimeField(blank=True, null=True, verbose_name="方案创建时间", auto_now_add=True)
    scheme_desc = models.TextField(blank=True, null=True, verbose_name="方案描述")
    # 第二页的参数
    # 2020-06-20
    driving_date = models.CharField(max_length=12, blank=True, null=True, verbose_name="行车选择日期")
    # '计划数据',"实际数据"
    driving_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="行车数据类型")
    # "2020-07-20"
    psflow_date = models.CharField(max_length=12, blank=True, null=True, verbose_name="客流选择日期")
    # 07:00:00
    start_time = models.CharField(max_length=10,blank=True, null=True, verbose_name="模拟车站的开始时间")
    # 09:00:00
    end_time = models.CharField(max_length=10,blank=True, null=True, verbose_name="模拟车站的结束时间")
    # 第三页的参数
    # "工作日早高峰"
    ps_pare_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='乘客参数状态类型')

    # 管理员
    editer = models.CharField(max_length=20, blank=True, null=True, verbose_name="修改人")
    # 修改时间
    edi_time = models.DateTimeField(blank=True, null=True, verbose_name="方案修改时间", auto_now=True)
    # 第四页的参数
    # 这个字段有问题
    is_run = models.CharField(max_length=5, blank=True, null=True, verbose_name="是否仿真完成")
    is_save = models.CharField(max_length=5, blank=True, null=True, verbose_name="仿真是否保存")
    is_3d = models.BooleanField(verbose_name='仿真是否是3D运行')
    class Meta:
        db_table = 'train_scheme'

class RePorts(models.Model):
    """仿真方案报告管理表"""
    reports_id = models.CharField(max_length=30, verbose_name='报告编号')
    scheme_id = models.CharField(max_length=30, verbose_name='仿真方案id')
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="选择开始时间")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="选择结束时间")
    reports_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="报告存储目录（包括文件夹和报告名称）")
    class Meta:
        db_table = 'reports'