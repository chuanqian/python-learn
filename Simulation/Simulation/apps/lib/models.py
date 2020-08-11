from django.db import models
class TransStation(models.Model):
    """换乘车站表"""
    station_id = models.CharField(max_length=4, verbose_name='车站id')
    line_id = models.CharField(max_length=2, verbose_name='线路名称')
    # 车站编码   0456 0256
    station_code = models.CharField(max_length=10, verbose_name='车站编码')
    """
    0232    苏州火车站   2号线   
    0432    苏州火车站   4号线
    0632    苏州火车站   6号线
    ------------------------
    0232    2号线   0232  
    0232    4号线   0432
    0232    6号线   0632

    0432    4号线   0432
    0442    2号线   0332
    0432    6号线   0632

    0632    6号线   0632
    0632    2号线   0232
    0632    4号线   0432
    """

    class Meta:
        db_table = 'trans_station'