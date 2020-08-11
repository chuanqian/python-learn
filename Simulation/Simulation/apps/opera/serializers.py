from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers

from . import models

class CommonListSerializer(ListSerializer):
    def update(self,instance,validated_data):
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

# 行车数据序列化
class TrainDataSerializer(ModelSerializer):
    class Meta:
        model = models.TrainData
        """
        线路
        车次号
        方向
        到站时间
        离站时间
        乘降时间
        上车人数
        下车人数
        到站满载率
        """
        fields = ('id','line_id','global_code','dir','arrive_time','depart_time','ride_time','up_number','down_number','arrive_load_rate')
# 进出客流序列化
class FlowInOutDetailSerializer(ModelSerializer):
    class Meta:
        model = models.FlowInOutDetail
        """
        线路编号
        方向
        统计时间
        乘降时间
        客流量
        """
        fields = ('id','line_id','dir','stat_tm','entry_quantity','exit_quantity')
# 进站客流序列化
class FlowInDetailSerializer(ModelSerializer):
    class Meta:
        model = models.FlowInOutDetail
        """
        线路编号
        方向
        统计时间
        乘降时间
        客流量
        """
        fields = ('id','line_id','dir','stat_tm','entry_quantity')
# 出站客流序列化
class FlowOutDetailSerializer(ModelSerializer):
    class Meta:
        model = models.FlowInOutDetail
        """
        线路编号
        方向
        统计时间
        乘降时间
        客流量
        """
        fields = ('id','line_id','dir','stat_tm','exit_quantity')
# 换乘客流序列化
class FlowTranDetailSerializer(ModelSerializer):
    class Meta:
        model = models.FlowTranDetail
        fields = ('id','from_line_id','to_line_id','from_drct_cd','to_drct_cd','stat_tm','quantity')

# 客流组织数据
class EmuGateStatusSerializer(ModelSerializer):
    class Meta:
        model = models.EmuGateStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')
        # list_serializer_class = CommonListSerializer
class GaSerializer(ModelSerializer):
    class Meta:
        model = models.EmuGateStatus
        fields = ('eq_id','eq_status')

class EmuEsCsStatusSerializer(ModelSerializer):
    class Meta:
        model = models.EmuEsCsStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')
        # list_serializer_class = CommonListSerializer

class EsSerializer(ModelSerializer):
    class Meta:
        model = models.EmuEsCsStatus
        fields = ('eq_id','eq_status')

class EmuFenceStatusSerializer(ModelSerializer):
    class Meta:
        model = models.EmuFenceStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')

class FenSerializer(ModelSerializer):
    class Meta:
        model = models.EmuFenceStatus
        fields = ('eq_id','eq_status')

class EmuGateWayStatusSerializer(ModelSerializer):
    class Meta:
        model = models.EmuGateWayStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status','orig_in_rate','var_in_rate','orig_out_rate','var_out_rate')
        list_serializer_class = CommonListSerializer

class WaySerializer(ModelSerializer):
    class Meta:
        model = models.EmuGateWayStatus
        fields = ('eq_id','eq_status')
# 车站基本参数
class EmuPsCompSerializer(ModelSerializer):
    class Meta:
        model = models.EmuPsComp
        fields = (
            'id','station_id','ps_pare_type','male_rate','female_rate','personal_rate','team_rate','older_rate','adult_rate','child_rate','no_bag_rate','small_bag_rate','big_bag_rate','mo_speed','mo_space','ma_speed','ma_space','mc_speed','mc_space','fo_speed','fo_space','fa_speed','fa_space','fc_speed','fc_space'
        )

class pParamSerializer(ModelSerializer):
    class Meta:
        model = models.EmuPsComp
        fields = (
            'male_rate','female_rate','personal_rate','team_rate','older_rate','adult_rate','child_rate','no_bag_rate','small_bag_rate','big_bag_rate','mo_speed','mo_space','ma_speed','ma_space','mc_speed','mc_space','fo_speed','fo_space','fa_speed','fa_space','fc_speed','fc_space'
        )

class EmuPsEquipmentSerializer(ModelSerializer):
    class Meta:
        model = models.EmuPsEquipment
        fields = (
            'id','station_id','ps_pare_type','no_use_rate','sc_fast_rate','sc_fast_rate','sc_big_bag_time','sc_small_bag_time','sc_fast_time','tvm_use_rate','tvm_tickets_rate','tvm_tickets_time','tvm_recharge_rate','tvm_recharge_time','bom_use_rate','bom_tickets_rate','bom_tickets_time','bom_recharge_rate','bom_recharge_time','gate_normal_time','gate_big_bag_time'
        )

class eParamSerializer(ModelSerializer):
    class Meta:
        model = models.EmuPsEquipment
        fields = (
            'sc_fast_rate','sc_big_bag_time','sc_small_bag_time','sc_fast_time','tvm_use_rate','tvm_tickets_rate','tvm_tickets_time','tvm_recharge_rate','tvm_recharge_time','bom_use_rate','bom_tickets_rate','bom_tickets_time','bom_recharge_rate','bom_recharge_time','gate_normal_time','gate_big_bag_time'
        )

class EmuPsFacilitiesSerializer(ModelSerializer):
    class Meta:
        model = models.EmuPsFacilities
        fields = (
            'id','station_id','ps_pare_type','stup_design_cap','stdown_design_cap','stmix_design_cap','esup_design_cap','esdown_design_cap','la_design_cap','el_design_cap','thsin_design_cap','thdou_design_cap','gasin_design_cap','gadou_design_cap','sc_design_cap'
        )

class EmuInOutRateSerializer(ModelSerializer):
    class Meta:
        model = models.EmuInOutRate
        fields = (
            'id','eq_id','station_id','ps_pare_type','in_rate','out_rate'
        )
        list_serializer_class = CommonListSerializer

class InOutSerializer(ModelSerializer):
    class Meta:
        model = models.EmuInOutRate
        fields = (
            'eq_id','out_rate','in_rate'
        )

class EmuTrainPartRateSerializer(ModelSerializer):
    """"""
    class Meta:
        model = models.EmuTrainPartRate
        fields = (
            'id','eq_id','station_id','ps_pare_type','direct_id','board_rate','getoff_rate'
        )
        list_serializer_class = CommonListSerializer

class PartSerializer(ModelSerializer):
    """"""
    class Meta:
        model = models.EmuTrainPartRate
        fields = (
            'eq_id','board_rate','getoff_rate'
        )