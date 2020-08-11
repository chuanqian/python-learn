from rest_framework.serializers import ModelSerializer,ListSerializer
from rest_framework import serializers

from . import models

class CommonListSerializer(ListSerializer):
    def update(self,instance,validated_data):
        for index,obj in enumerate(instance):
            self.child.update(obj,validated_data[index])
        return instance

class GateStatusSerializer(ModelSerializer):
    class Meta:
        model = models.GateStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')
        # list_serializer_class = CommonListSerializer

class EsCsStatusSerializer(ModelSerializer):
    class Meta:
        model = models.EsCsStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')
        # list_serializer_class = CommonListSerializer

class FenceStatusSerializer(ModelSerializer):
    class Meta:
        model = models.FenceStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status')
        # list_serializer_class = CommonListSerializer

class GateWayStatusSerializer(ModelSerializer):
    class Meta:
        model = models.GateWayStatus
        fields = ('id','eq_id','equ_name','station_id','ps_pare_type','loc','eq_status','orig_in_rate','var_in_rate','orig_out_rate','var_out_rate')
        list_serializer_class = CommonListSerializer

class PsCompSerializer(ModelSerializer):
    class Meta:
        model = models.PsComp
        fields = (
            'id','station_id','ps_pare_type','male_rate','female_rate','personal_rate','team_rate','older_rate','adult_rate','child_rate','no_bag_rate','small_bag_rate','big_bag_rate','mo_speed','mo_space','ma_speed','ma_space','mc_speed','mc_space','fo_speed','fo_space','fa_speed','fa_space','fc_speed','fc_space'
        )

class PsEquipmentSerializer(ModelSerializer):
    class Meta:
        model = models.PsEquipment
        fields = (
            'id','station_id','ps_pare_type','no_use_rate','sc_fast_rate','sc_big_bag_time','sc_small_bag_time','sc_fast_time','tvm_use_rate','tvm_tickets_rate','tvm_tickets_time','tvm_recharge_rate','tvm_recharge_time','bom_use_rate','bom_tickets_rate','bom_tickets_time','bom_recharge_rate','bom_recharge_time','gate_normal_time','gate_big_bag_time'
        )

class PsFacilitiesSerializer(ModelSerializer):
    class Meta:
        model = models.PsFacilities
        fields = (
            'id','station_id','ps_pare_type','stup_design_cap','stdown_design_cap','stmix_design_cap','esup_design_cap','esdown_design_cap','la_design_cap','el_design_cap','thsin_design_cap','thdou_design_cap','gasin_design_cap','gadou_design_cap','sc_design_cap'
        )

class InOutRateSerializer(ModelSerializer):
    class Meta:
        model = models.InOutRate
        fields = (
            'id','eq_id','station_id','ps_pare_type','in_rate','out_rate'
        )
        list_serializer_class = CommonListSerializer

class TrainPartRateSerializer(ModelSerializer):
    """"""
    class Meta:
        model = models.TrainPartRate
        fields = (
            'id','eq_id','station_id','ps_pare_type','direct_id','board_rate','getoff_rate'
        )
        list_serializer_class = CommonListSerializer