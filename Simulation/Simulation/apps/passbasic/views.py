from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from Simulation.utils.response import APIResponse
from passbasic import models
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from lib.models import TransStation
# /opera/gate/
class GateStatusAPIView(ListAPIView):
    """闸机"""
    queryset = models.GateStatus.objects.all()
    serializer_class = serializers.GateStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id','ps_pare_type']

    def get(self,request,*args,**kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_gate_obj = models.GateStatus.objects.filter(pk=pk).first()

        gate_ser = serializers.GateStatusSerializer(instance=old_gate_obj, data=request_data, partial=True)
        gate_ser.is_valid(raise_exception=True)
        gate_obj = gate_ser.save()
        results = serializers.GateStatusSerializer(gate_obj).data
        return APIResponse(results=results)

# /opera/es/
class EsCsStatusAPIView(ListAPIView):
    """扶梯"""
    queryset = models.EsCsStatus.objects.all()
    serializer_class = serializers.EsCsStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_es_obj = models.EsCsStatus.objects.filter(pk=pk).first()

        es_ser = serializers.EsCsStatusSerializer(instance=old_es_obj, data=request_data, partial=True)
        es_ser.is_valid(raise_exception=True)
        es_obj = es_ser.save()
        results = serializers.EsCsStatusSerializer(es_obj).data
        return APIResponse(results=results)

# /opera/fen/
class FenceStatusAPIView(ListAPIView):
    """导流栏"""
    queryset = models.FenceStatus.objects.all()
    serializer_class = serializers.FenceStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_fen_obj = models.FenceStatus.objects.filter(pk=pk).first()

        fen_ser = serializers.FenceStatusSerializer(instance=old_fen_obj, data=request_data, partial=True)
        fen_ser.is_valid(raise_exception=True)
        fen_obj = fen_ser.save()
        results = serializers.FenceStatusSerializer(fen_obj).data
        return APIResponse(results=results)

# /opera/way/
class GateWayStatusAPIView(ListAPIView):
    """出入口"""
    queryset = models.GateWayStatus.objects.all()
    serializer_class = serializers.GateWayStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)
    # 群改
    def patch(self, request, *args, **kwargs):
        # 多条数据局部修改数据
        way_list = request.data.get('way_list')
        length = len(way_list)
        if not length:
            return APIResponse(0, 'way_list is None')
        # 单改
        if length == 1:  # 单改
            # 获取修改的字典
            data_dict = way_list[0]
            # 弹出id值
            pk = data_dict.pop('id', None)
            pks = [pk, ]
            # 把数据放入列表中
            way_list = [data_dict, ]
        # 如果pk不存在，就是多条数据局部修改
        else:
            pks = []
            # 循环前端的多条数据 获取到的时一个个字典
            for dic in way_list:
                # 从字典中取出对象的id值
                pk = dic.pop('id', None)
                if pk:
                    # 如果id值存在，追加
                    pks.append(pk)
                else:
                    return APIResponse(0, 'id not in dic on the way_list')
        objs = []
        new_request_data = []
        # 从id值列表中取出索引和数组中的值
        for index, pk in enumerate(pks):
            try:
                obj = models.GateWayStatus.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(way_list[index])
            except Exception as e:
                print(e)
                continue

        way_ser = serializers.GateWayStatusSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        way_ser.is_valid(raise_exception=True)
        way_objs = way_ser.save()
        results = serializers.GateWayStatusSerializer(way_objs, many=True).data
        return APIResponse(results=results)

# /opera/pscomp/
class PsCompAPIView(APIView):
    """乘客基本属性"""
    def get(self,request,*args,**kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')

        if not (station_id and ps_pare_type):
            return APIResponse(0,'maybe only having a param is null')

        ps_obj = models.PsComp.objects.filter(station_id=station_id,ps_pare_type=ps_pare_type).first()

        if not ps_obj:
            return APIResponse(0,'the data in the database is empty')

        ps_data = serializers.PsCompSerializer(ps_obj).data

        return APIResponse(results=ps_data)

    # 单条数据的全部修改
    def put(self,request,*args,**kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0,'the param is null')

        pk = request_data.get('id')
        old_ps_obj = models.PsComp.objects.filter(pk=pk).first()

        ps_ser = serializers.PsCompSerializer(instance=old_ps_obj, data=request_data, partial=False)
        ps_ser.is_valid(raise_exception=True)
        ps_obj = ps_ser.save()
        results = serializers.PsCompSerializer(ps_obj).data
        return APIResponse(results=results)

# /opera/psequ/
class PsEquipmentAPIView(APIView):
    """设备使用信息"""

    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')

        if not (station_id and ps_pare_type):
            return APIResponse(0, 'maybe only having a param is null')

        euq_obj = models.PsEquipment.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type).first()

        if not euq_obj:
            return APIResponse(0, 'the data in the database is empty')

        equ_data = serializers.PsEquipmentSerializer(euq_obj).data

        return APIResponse(results=equ_data)

    # 单条数据的全部修改
    def put(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_equ_obj = models.PsEquipment.objects.filter(pk=pk).first()

        equ_ser = serializers.PsEquipmentSerializer(instance=old_equ_obj, data=request_data, partial=False)
        equ_ser.is_valid(raise_exception=True)
        equ_obj = equ_ser.save()
        results = serializers.PsEquipmentSerializer(equ_obj).data
        return APIResponse(results=results)

# /opera/psfac/
class PsFacilitiesAPIView(APIView):
    """设备设施能力"""
    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')

        if not (station_id and ps_pare_type):
            return APIResponse(0, 'maybe only having a param is null')

        fac_obj = models.PsFacilities.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type).first()

        if not fac_obj:
            return APIResponse(0, 'the data in the database is empty')

        fac_data = serializers.PsFacilitiesSerializer(fac_obj).data

        return APIResponse(results=fac_data)

    # 单条数据的全部修改
    def put(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_fac_obj = models.PsFacilities.objects.filter(pk=pk).first()

        fac_ser = serializers.PsFacilitiesSerializer(instance=old_fac_obj, data=request_data, partial=False)
        fac_ser.is_valid(raise_exception=True)
        fac_obj = fac_ser.save()
        results = serializers.PsFacilitiesSerializer(fac_obj).data
        return APIResponse(results=results)

# /opera/inout/
class InOutRateAPIView(APIView):
    """出入口比例"""
    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')
        if not (station_id and ps_pare_type):
            return APIResponse(0, 'The params is null')

        out_query = models.InOutRate.objects.filter(
            station_id=station_id,
            ps_pare_type=ps_pare_type,
        ).all()

        if not out_query:
            return APIResponse(0, 'the data in the database is empty')

        in_out_query = models.InOutRate.objects.filter(
            station_id=station_id,
            ps_pare_type=ps_pare_type,
        ).all()

        if not in_out_query:
            return APIResponse(0, 'the data in the database is empty')

        in_data = serializers.InOutRateSerializer(in_out_query, many=True).data

        return APIResponse(in_data=in_data, out_data=in_data)

    def put(self, request, *args, **kwargs):
        ent_list = request.data.get('ent_list')
        length = len(ent_list)
        if not length:
            return APIResponse(0,'ent_list is None')
        # 单改
        if length == 1:  # 单改
            # 获取修改的字典
            data_dict = ent_list[0]
            # 弹出id值
            pk = data_dict.pop('id', None)
            pks = [pk, ]
            # 把数据放入列表中
            ent_list = [data_dict, ]
        # 如果pk不存在，就是多条数据局部修改
        else:
            pks = []
            # 循环前端的多条数据 获取到的时一个个字典
            for dic in ent_list:
                # 从字典中取出对象的id值
                pk = dic.pop('id', None)
                if pk:
                    # 如果id值存在，追加
                    pks.append(pk)
                else:
                    return APIResponse(0, 'id not in dic on the ent_list')
        objs = []
        new_request_data = []
        # 从id值列表中取出索引和数组中的值
        for index, pk in enumerate(pks):
            try:
                obj = models.InOutRate.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(ent_list[index])
            except Exception as e:
                print(e)
                continue
        ent_ser = serializers.InOutRateSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        ent_ser.is_valid(raise_exception=True)
        ent_objs = ent_ser.save()
        results = serializers.InOutRateSerializer(ent_objs, many=True).data
        return APIResponse(results=results)

# /opera/trainpart/
class TrainPartRateAPIView(APIView):
    """车厢选择比例"""
    def get(self, request, *args, **kwargs):
        # 这个是换乘站的标识
        station_type = request.query_params.get('station_type')
        # 车站的编码
        station_id = request.query_params.get('station_id')
        # 峰值类型
        ps_pare_type = request.query_params.get('ps_pare_type')
        if not (station_id and ps_pare_type and station_type):
            return APIResponse(0,'The params is null')

        if station_type not in ["换乘车站",'非换乘车站']:
            return APIResponse(0,'station_type is false')

        if station_type == '非换乘车站':
            # 上行query对象
            up_query = models.TrainPartRate.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type,direct_id="上行").all()
            if not up_query:
                return APIResponse(0,"the data in the database is empty")
            # 下行query对象
            down_query = models.TrainPartRate.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type,direct_id="下行").all()
            # 上行数据
            up_data = serializers.TrainPartRateSerializer(up_query,many=True).data
            # 下行数据
            down_data = serializers.TrainPartRateSerializer(down_query,many=True).data
            return APIResponse(up_data=up_data,down_data=down_data)

        else:
            # 换乘车站信息
            trans_query = TransStation.objects.filter(station_id=station_id).values_list('station_code',flat=True)
            if not trans_query:
                return APIResponse(0,'the data in the database is empty')
            # 换乘车站列表
            trans_list = list(trans_query)
            print(trans_list)
            # 车厢比例  __in 是取这个列表中所有的数据
            tra_query = models.TrainPartRate.objects.filter(station_id__in=trans_list,ps_pare_type=ps_pare_type).all()
            if not tra_query:
                return APIResponse(0,'the data in the database is empty')
            data_list = []
            for tra in tra_query:
                emutra_data = serializers.TrainPartRateSerializer(tra).data
                data_list.append(emutra_data)

            return APIResponse(2,results=data_list)

    def put(self, request, *args, **kwargs):
        part_list = request.data.get('part_list')
        length = len(part_list)
        if not length:
            return APIResponse(0,'part_list is None')
        # 单改
        if length == 1:  # 单改
            # 获取修改的字典
            data_dict = part_list[0]
            # 弹出id值
            pk = data_dict.pop('id', None)
            pks = [pk, ]
            # 把数据放入列表中
            part_list = [data_dict, ]
        # 如果pk不存在，就是多条数据局部修改
        else:
            pks = []
            # 循环前端的多条数据 获取到的时一个个字典
            for dic in part_list:
                # 从字典中取出对象的id值
                pk = dic.pop('id', None)
                if pk:
                    # 如果id值存在，追加
                    pks.append(pk)
                else:
                    return APIResponse(0, 'id not in dic on the part_list')
        objs = []
        new_request_data = []
        # 从id值列表中取出索引和数组中的值
        for index, pk in enumerate(pks):
            try:
                obj = models.TrainPartRate.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(part_list[index])
            except Exception as e:
                print(e)
                continue

        part_ser = serializers.TrainPartRateSerializer(instance=objs, data=new_request_data, partial=True, many=True)
        part_ser.is_valid(raise_exception=True)
        part_objs = part_ser.save()
        results = serializers.TrainPartRateSerializer(part_objs, many=True).data
        return APIResponse(results=results)