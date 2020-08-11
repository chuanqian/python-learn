from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers
from . import models

class CommonListSerializer(ListSerializer):
    def update(self,instance,validated_data):
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

class TrainLineSerializer(ModelSerializer):
    class Meta:
        model = models.TrainLine
        fields = ('line_id','line_name','station_list')

class TrainStationSerializer(ModelSerializer):
    class Meta:
        model = models.TrainStation
        fields = ('station_id','line','station_name','des','station_type','pf_type','passages_num','station_pic','current_model_version','model_version_create_time','sim_station_name','wo_peak_hours','ho_peak_hours')

class ModelVersionSerializer(ModelSerializer):
    # update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # 版本号
    # ver_num = serializers.CharField(write_only=True)
    class Meta:
        model = models.ModelVersion
        fields = (
            'id','version_number','founder','create_time','version_des','current_model_version'
        )
        # 反序列化校验
        # extra_kwargs = {
        #     'ver_num': {
        #         "write_only": True,
        #     },
        #     'model_url': {
        #         "write_only": True,
        #     },
        # }

class StationImageSerializer(ModelSerializer):
    class Meta:
        model = models.StationImage
        fields = (
            'id','image_name','image_format','image_url','founder','create_time','current_image_name'
        )

class TrainSchemeSerializer(ModelSerializer):
    """仿真方案的序列化组件"""
    class Meta:
        model = models.TrainScheme
        fields = ("scheme_id","scheme_type","scheme_name",'station_id','station_name',"driving_date","driving_type",'psflow_date',"start_time","end_time","ps_pare_type",'creater',"create_time",'editer','edi_time',"is_run",'is_save',"scheme_desc")




