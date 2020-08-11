from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from Simulation.utils.response import APIResponse
from django.http import JsonResponse
from Simulation.libs import common
from . import models
import xlrd
from station_info.models import TrainScheme
from passbasic.models import GateStatus,EsCsStatus,FenceStatus,GateWayStatus,PsComp,PsEquipment,PsFacilities,InOutRate,TrainPartRate
from django.db.models import Sum
from . import serializers
from lib.center_models import FlowInOut15m,FlowTran15m,TrainPlan,TrainReality
from lib.models import TransStation
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from django.http import StreamingHttpResponse
from django.db import connection
cursor=connection.cursor()
import os,json
from settings.dev import MEDIA_ROOT,LINE_DIC,DOWNLOAD
import logging
logger = logging.getLogger('logger')
# from kafka import KafkaProducer
class PsRequest(APIView):
    # 客流数据获取
    def get(self,request,*args,**kwargs):
        # "2020-05-20"
        date = request.query_params.get('date')
        # ["07:00","09:00"]
        period_list = request.query_params.get('period_list')
        # print(period_list)
        # "fakjfakfjf"
        scheme_id = request.query_params.get('scheme_id')
        # "非换乘车站"  "换乘车站"
        station_type = request.query_params.get('station_type')
        # "0101"  "0120"
        station_id = request.query_params.get('station_id')


        if not (date and period_list and scheme_id and station_type and station_id):
            return APIResponse(0, 'the param maybe just not full data')

        if station_type not in ['非换乘车站',"换乘车站"]:
            return APIResponse(0,"station_type not a correct param")
        period_list = period_list.split(' ')
        if len(period_list) != 2:
            return APIResponse(0,'period_list not two param')
        # 这是在数据中心的数据库中的start_time 和 end_tm中的数据类型为"07:00:00"这种形式的时候
        first_tm,second_tm = period_list
        start_tm = first_tm + ":00"
        end_tm = second_tm + ":00"
        # 这块可能需要再做处理
        # 获取某个时间段的15分钟的索引代码
        belong_fif_min_index_cd_query = models.BaseStatIndexCd.objects.filter(start_tm__gte=start_tm,end_tm__lte=end_tm).values_list("belong_fif_min_index_cd",flat=True).distinct()
        # 某个时间段的所有索引代码 是一个列表
        belong_fif_min_index_cd_list = list(belong_fif_min_index_cd_query)
        base_index_dic = {}
        # 获取的是一个个的索引代码
        for belong_fif_min_index_cd in belong_fif_min_index_cd_list:
            # 根据15分钟时段索引代码查询出对象，获取最后一个的stat_end_time
            stat_end_time = models.BaseStatIndexCd.objects.filter(belong_fif_min_index_cd=belong_fif_min_index_cd).first().stat_end_tm
            base_index_dic[belong_fif_min_index_cd] = stat_end_time

        if station_type == "非换乘车站":
            station_list = [station_id]
        else:
            trans_station_query = TransStation.objects.filter(station_id=station_id).values_list("station_code",flat=True)
            if not trans_station_query:
                return APIResponse(0,"the data in the database is empty")
            station_list = list(trans_station_query)

        # 每个索引时段代码下的总的进出客流量
        flow_query = FlowInOut15m.objects.using("slave").filter(data_dt=date,station_id__in=station_list,stat_index_cd__in=belong_fif_min_index_cd_list).values("stat_index_cd").annotate(entry=Sum('entry_quantity'),exit=Sum('exit_quantity')).values('line_id','stat_index_cd','station_id','entry','exit')
        if not flow_query:
            return APIResponse(0,"the flowinout database is empty")
        data_list = []
        for flow in flow_query:
            data_dic = {
                "scheme_id":scheme_id,
                "line_id":flow.get('line_id'),
                "station_id":flow.get('station_id'),
                "stat_tm":date+" "+base_index_dic.get(f'{flow.get("stat_index_cd")}'),
                "entry_quantity":flow.get('entry'),
                "exit_quantity":flow.get("exit"),
                # "dir":flow.dir
            }
            data_list.append(data_dic)

        for data_dic in data_list:
            # 写入进出站的表中
            models.FlowInOutDetail.objects.create(**data_dic)
        if station_type == "非换乘车站":
            return APIResponse(1,"the data send to the databases success")
        # trans_station_query = TransStation.objects.filter(station_id=station_id).values_list("station_code",flat=True)
        # if not trans_station_query:
        #     return APIResponse(0,"the data in the database is empty")
        # trans_station_list = list(trans_station_query)
        # 获取的是一个列表套对象的形式[object1,object2]
        # trans_flow_query = FlowInOut15m.objects.using("slave").filter(data_dt=date, station_id__in=station_list,stat_index_cd__in=belong_fif_min_index_cd_list).all()
        # if not trans_flow_query:
        #     return APIResponse(0, "the database is empty")
        # trans_flow_list = []
        # for trans_flow in trans_flow_query:
        #     trans_flow_dic = {
        #         "scheme_id": scheme_id,
        #         "line_id": trans_flow.line_id,
        #         "station_id": station_id,
        #         "stat_tm": date + " " + base_index_dic.get(f"{trans_flow.stat_index_cd}"),
        #         "entry_quantity": trans_flow.entry_quantity,
        #         "exit_quantity": trans_flow.exit_quantity,
        #         "dir": trans_flow.dir
        #     }
        #     trans_flow_list.append(trans_flow_dic)
        #
        # for trans_flow_dic in trans_flow_list:
        #     models.FlowInOutDetail.objects.create(**trans_flow_dic)
        # 获取非换乘车站的换乘客流数据
        flow_tran_query = FlowTran15m.objects.using("slave").filter(data_dt=date, station_id__in=station_list,stat_index_cd__in=belong_fif_min_index_cd_list).values("stat_index_cd").annotate(quant=Sum('quantity')).values('stat_index_cd','from_line_id','to_line_id','from_drct_cd','to_drct_cd','quant','station_id')
        # print(flow_tran_query)
        if not flow_tran_query:
            return APIResponse(0, "the data on the database is None")
        trans_data_list = []
        for flow_tran in flow_tran_query:
            data_dic = {
                "scheme_id": scheme_id,
                "from_line_id": flow_tran.get('from_line_id'),
                "to_line_id": flow_tran.get('to_line_id'),
                "from_drct_cd": flow_tran.get('from_drct_cd'),
                "to_drct_cd": flow_tran.get('to_drct_cd'),
                "station_id": flow_tran.get('station_id'),
                "stat_tm": date + " " + base_index_dic.get(f"{flow_tran.get('stat_index_cd')}"),
                "quantity": flow_tran.get('quant'),
            }
            # print(flow_tran.get('stat_index_cd'))
            trans_data_list.append(data_dic)

        for trans_data in trans_data_list:
            models.FlowTranDetail.objects.create(**trans_data)
        return APIResponse(1, "the data send to the databases success")

    # 客流数据预设  换乘车站和非换乘车站
    def post(self,request,*args,**kwargs):
        # 时段选择
        period_list = request.data.get('period_list')
        # 方案id
        scheme_id = request.data.get('scheme_id')
        # "非换乘车站"  "换乘车站"  车站类型
        station_type = request.data.get('station_type')
        # "0101"  "0120"   车站id
        station_id = request.data.get('station_id')
        entry_quantity = request.data.get('entry_quantity')
        exit_quantity = request.data.get('exit_quantity')
        if not (period_list and scheme_id and station_type and station_id and entry_quantity and exit_quantity):
            return APIResponse(0,'The post request has missing parameters')

        first_time,second_time = period_list
        start_tm = first_time + ":00"
        end_tm = second_time + ":00"
        # 根据时间段获取所有的开始结束时间
        stat_end_tm = models.BaseStatIndexCd.objects.filter(start_tm__gte=start_tm,end_tm__lte=end_tm).values_list("stat_end_tm",flat=True)
        if not stat_end_tm:
            return APIResponse(0,'the database is empty')

        stat_end_tm_list = list(stat_end_tm)
        # 当前车站的数据
        data_list = []
        # 循环这个开始结束时间 组织数据
        for stat_end_tm in stat_end_tm_list:
            # 日期字符串
            date = str(datetime.datetime.now().date())
            data_dic = {
                "line_id":station_id[:2],
                "station_id":station_id,
                "stat_tm":date +" "+stat_end_tm,
                "entry_quantity":entry_quantity,
                "exit_quantity":exit_quantity,
                "dir":"01",
                "scheme_id":scheme_id
            }
            data_dic1 = {
                "line_id": station_id[:2],
                "station_id": station_id,
                "stat_tm": date + " " + stat_end_tm,
                "entry_quantity": entry_quantity,
                "exit_quantity": exit_quantity,
                "dir": "02",
                "scheme_id": scheme_id
            }
            data_list.append(data_dic)
            data_list.append(data_dic1)

        for data_dic in data_list:
            models.FlowInOutDetail.objects.create(**data_dic)

        if station_type == "非换乘车站":
            return APIResponse(1,'the data save into database')

        quantity = request.data.get('quantity')
        if not quantity:
            return APIResponse(0, 'quantity is exist')
        trans_station_query = TransStation.objects.filter(station_id=station_id).all()
        if not trans_station_query:
            return APIResponse(0,'换乘数据不存在')
        first_trans_station_id,second_trans_station_id = trans_station_query

        if first_trans_station_id.station_code == station_id:
            # # 当前车站id
            station_code = second_trans_station_id.station_code
        else:
            # 换乘车站id
            station_code = first_trans_station_id.station_code

        flow_data_list = []
        # 循环这个开始结束时间 组织数据
        for stat_end_tm in stat_end_tm_list:
            # 日期字符串
            date = str(datetime.datetime.now().date())
            flow_data_dic = {
                "line_id":station_code[:2],
                "station_id":station_code,
                "stat_tm":date +" "+stat_end_tm,
                "entry_quantity":entry_quantity,
                "exit_quantity":exit_quantity,
                "dir":"01",
                "scheme_id":scheme_id
            }
            flow_data_dic1 = {
                "line_id": station_code[:2],
                "station_id": station_code,
                "stat_tm": date + " " + stat_end_tm,
                "entry_quantity": entry_quantity,
                "exit_quantity": exit_quantity,
                "dir": "02",
                "scheme_id": scheme_id
            }
            flow_data_list.append(flow_data_dic)
            flow_data_list.append(flow_data_dic1)

        trans_data_list = []
        for stat_end_tm in stat_end_tm_list:
            date = str(datetime.datetime.now().date())
            trans_data_dic = {
                "station_id":first_trans_station_id.station_code,
                "stat_tm":date +" "+stat_end_tm,
                "from_line_id":first_trans_station_id.line_id,
                "to_line_id":second_trans_station_id.line_id,
                "from_drct_cd":"01",
                "to_drct_cd":"01",
                "quantity":quantity,
                "scheme_id":scheme_id
            }
            trans_data_dic1 = {
                "station_id":first_trans_station_id.station_code,
                "stat_tm":date +" "+stat_end_tm,
                "from_line_id":first_trans_station_id.line_id,
                "to_line_id":second_trans_station_id.line_id,
                "from_drct_cd":"01",
                "to_drct_cd":"02",
                "quantity":quantity,
                "scheme_id":scheme_id
            }
            trans_data_dic2 = {
                "station_id": first_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": first_trans_station_id.line_id,
                "to_line_id": second_trans_station_id.line_id,
                "from_drct_cd": "02",
                "to_drct_cd": "01",
                "quantity":quantity,
                "scheme_id": scheme_id
            }
            trans_data_dic3 = {
                "station_id": first_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": first_trans_station_id.line_id,
                "to_line_id": second_trans_station_id.line_id,
                "from_drct_cd": "02",
                "to_drct_cd": "02",
                "quantity":quantity,
                "scheme_id": scheme_id
            }
            trans_data_dic4 = {
                "station_id": second_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": second_trans_station_id.line_id,
                "to_line_id": first_trans_station_id.line_id,
                "from_drct_cd": "01",
                "to_drct_cd": "01",
                "quantity": quantity,
                "scheme_id": scheme_id
            }
            trans_data_dic5 = {
                "station_id": second_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": second_trans_station_id.line_id,
                "to_line_id": first_trans_station_id.line_id,
                "from_drct_cd": "01",
                "to_drct_cd": "02",
                "quantity": quantity,
                "scheme_id": scheme_id
            }
            trans_data_dic6 = {
                "station_id": second_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": second_trans_station_id.line_id,
                "to_line_id": first_trans_station_id.line_id,
                "from_drct_cd": "02",
                "to_drct_cd": "01",
                "quantity":quantity,
                "scheme_id": scheme_id
            }
            trans_data_dic7 = {
                "station_id": second_trans_station_id.station_code,
                "stat_tm": date + " " + stat_end_tm,
                "from_line_id": second_trans_station_id.line_id,
                "to_line_id": first_trans_station_id.line_id,
                "from_drct_cd": "02",
                "to_drct_cd": "02",
                "quantity":quantity,
                "scheme_id": scheme_id
            }

            trans_data_list.append(trans_data_dic)
            trans_data_list.append(trans_data_dic1)
            trans_data_list.append(trans_data_dic2)
            trans_data_list.append(trans_data_dic3)
            trans_data_list.append(trans_data_dic4)
            trans_data_list.append(trans_data_dic5)
            trans_data_list.append(trans_data_dic6)
            trans_data_list.append(trans_data_dic7)

        for flow_data in flow_data_list:
            models.FlowInOutDetail.objects.create(**flow_data)

        for trans_data in trans_data_list:
            models.FlowTranDetail.objects.create(**trans_data)

        return APIResponse(1,'进出站和换乘数据录入成功')

class DrRequest(APIView):
    # 行车数据获取
    def get(self, request, *args, **kwargs):
        # "2020-05-20"
        date = request.query_params.get('date')
        # '["07:00","09:00"]  "07:00 09:00"
        period_list = request.query_params.get('period_list')
        # "fakjfakfjf"
        scheme_id = request.query_params.get('scheme_id')
        # "非换乘车站"  "换乘车站"
        station_type = request.query_params.get('station_type')
        # "0101"  "0120"
        station_id = request.query_params.get('station_id')
        # "计划数据"  "实际数据"
        category = request.query_params.get('type')

        if not (date and period_list and scheme_id and station_type and station_id and category):
            return APIResponse(0, 'the param maybe just not full data')

        if station_type not in ['非换乘车站', "换乘车站"]:
            return APIResponse(0, "station_type not a correct param")
        # 为了测试
        period_list = period_list.split(" ")
        if len(period_list) != 2:
            return APIResponse(0, 'period_list not two param')

        if category not in ["计划数据",'实际数据']:
            return APIResponse(0,'type date maybe error')
        # "07:00"   "09:00"
        # print(period_list)
        first_time, second_time = period_list
        # "2020-06-20 07:00"
        start_time_str = date + " " + first_time + ":00"
        # datetime类型
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %X')
        end_time_str = date + " " + second_time + ":00"
        end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %X')
        # date_list = [start_time, end_time]

        if station_type == "非换乘车站":
            if category == "计划数据":
                db_plan_query = TrainPlan.objects.using('slave').filter(station_id=station_id,arrive_time__gte=start_time,arrive_time__lte=end_time).all()
                if not db_plan_query:
                    return APIResponse(0,"the data on the database is empty")
                data_list = []
                for plan_query in db_plan_query:
                    data_dic = {
                        "scheme_id":scheme_id,
                        "station_id":station_id,
                        "platform":plan_query.platform,
                        "group_code":plan_query.group_code,
                        "line_id":plan_query.line_id,
                        "global_code":plan_query.global_code,
                        "dir":plan_query.dir,
                        "arrive_time":str(plan_query.arrive_time),
                        "depart_time":str(plan_query.depart_time),
                        "ride_time":plan_query.ride_time,
                        "up_number":plan_query.up_number,
                        "down_number":plan_query.down_number,
                        "arrive_load_rate":plan_query.arrive_load_rate,
                        "depart_load_rate":plan_query.depart_load_rate,
                    }
                    data_list.append(data_dic)

                for data_dic in data_list:
                    models.TrainData.objects.create(**data_dic)

                return APIResponse(1,"the data send to database is success")

            db_reality_query = TrainReality.objects.using("slave").filter(station_id=station_id,arrive_time__gte=start_time,arrive_time__lte=end_time).all()
            if not db_reality_query:
                return APIResponse(0, "the data on the database is empty")
            data_list = []
            for reality_query in db_reality_query:
                data_dic = {
                    "scheme_id": scheme_id,
                    "station_id": station_id,
                    "platform": reality_query.platform,
                    "group_code": reality_query.group_code,
                    "line_id": reality_query.line_id,
                    "global_code": reality_query.global_code,
                    "dir": reality_query.dir,
                    "arrive_time": str(reality_query.arrive_time),
                    "depart_time": str(reality_query.depart_time),
                    "ride_time": reality_query.ride_time,
                    "up_number": reality_query.up_number,
                    "down_number": reality_query.down_number,
                    "arrive_load_rate": reality_query.arrive_load_rate,
                    "depart_load_rate": reality_query.depart_load_rate,
                }
                data_list.append(data_dic)

            for data_dic in data_list:
                models.TrainData.objects.create(**data_dic)

            return APIResponse(1,"the data send to database is success")

        trans_station_query = TransStation.objects.filter(station_id=station_id).values_list("station_code",flat=True)
        if not trans_station_query:
            return APIResponse(0, "the data in the database is empty")

        trans_station_list = list(trans_station_query)
        # print(trans_station_list)
        if category == "计划数据":
            db_plan_query = TrainPlan.objects.using('slave').filter(station_id__in=trans_station_list,arrive_time__gte=start_time, arrive_time__lte=end_time).all()
            if not db_plan_query:
                return APIResponse(0, "the data on the database is empty")
            data_list = []
            for plan_query in db_plan_query:
                data_dic = {
                    "scheme_id": scheme_id,
                    "station_id": plan_query.station_id,
                    "platform": plan_query.platform,
                    "group_code": plan_query.group_code,
                    "line_id": plan_query.line_id,
                    "global_code": plan_query.global_code,
                    "dir": plan_query.dir,
                    "arrive_time": str(plan_query.arrive_time),
                    "depart_time": str(plan_query.depart_time),
                    "ride_time": plan_query.ride_time,
                    "up_number": plan_query.up_number,
                    "down_number": plan_query.down_number,
                    "arrive_load_rate": plan_query.arrive_load_rate,
                    "depart_load_rate": plan_query.depart_load_rate,
                }
                data_list.append(data_dic)

            for data_dic in data_list:
                models.TrainData.objects.create(**data_dic)

            return APIResponse(1, "the data send to database is success")

        db_reality_query = TrainReality.objects.using("slave").filter(station_id__in=trans_station_list,arrive_time__gte=start_time,
                                                                      arrive_time__lte=end_time).all()
        if not db_reality_query:
            return APIResponse(0, "the data on the database is empty")
        data_list = []
        for reality_query in db_reality_query:
            data_dic = {
                "scheme_id": scheme_id,
                "station_id": reality_query.station_id,
                "platform": reality_query.platform,
                "group_code": reality_query.group_code,
                "line_id": reality_query.line_id,
                "global_code": reality_query.global_code,
                "dir": reality_query.dir,
                "arrive_time": str(reality_query.arrive_time),
                "depart_time": str(reality_query.depart_time),
                "ride_time": reality_query.ride_time,
                "up_number": reality_query.up_number,
                "down_number": reality_query.down_number,
                "arrive_load_rate": reality_query.arrive_load_rate,
                "depart_load_rate": reality_query.depart_load_rate,
            }
            data_list.append(data_dic)

        for data_dic in data_list:
            models.TrainData.objects.create(**data_dic)
        return APIResponse(1, "the data send to database is success")
    # 行车数据预设
    def post(self,request,*args,**kwargs):
        # ["07:00","09:00"]
        period_list = request.data.get('period_list')
        # "fakjfakfjf"
        scheme_id = request.data.get('scheme_id')
        # "非换乘车站"  "换乘车站"
        station_type = request.data.get('station_type')
        # "0101"  "0120"
        station_id = request.data.get('station_id')
        # 发车间隔
        de_inter = request.data.get('de_inter')
        ride_time = request.data.get('ride_time')
        up_number = request.data.get('up_number')
        down_number = request.data.get('down_number')
        arrive_load_rate = request.data.get('arrive_load_rate')
        # "计划数据"  "实际数据"
        if not (period_list and scheme_id and station_type and station_id and de_inter and ride_time and up_number and down_number and arrive_load_rate):
            return APIResponse(0, 'the param maybe just not full data')

        if station_type not in ['非换乘车站', "换乘车站"]:
            return APIResponse(0, "station_type not a correct param")

        if len(period_list) != 2:
            return APIResponse(0, 'period_list not two param')
        # "07:00"   "09:00"
        first_time, second_time = period_list
        # 获取到达时间 和 离去是时间
        res_list = common.get_data_list(first_time,second_time,de_inter,ride_time)
        global_code = 1000
        # 非换乘车站的数据 以及 换乘车站的数据
        data_list = []
        for res in res_list:
            dic = {
                "line_id":station_id[:2],
                "station_id":station_id,
                "global_code":str(global_code),
                "dir":"1",
                "up_number":up_number,
                "down_number":down_number,
                "arrive_load_rate":arrive_load_rate,
                'scheme_id':scheme_id,
            }
            dic.update(res)
            dic2 = {
                "line_id": station_id[:2],
                "station_id": station_id,
                "global_code": str(global_code),
                "dir": "2",
                "up_number": up_number,
                "down_number": down_number,
                "arrive_load_rate": arrive_load_rate,
                'scheme_id': scheme_id,
            }
            dic2.update(res)
            data_list.append(dic)
            data_list.append(dic2)
            global_code += 1
        for data_dic in data_list:
            models.TrainData.objects.create(**data_dic)

        if station_type == "非换乘车站":
            return APIResponse(1,'数据预设完成')

        trans_query = TransStation.objects.filter(station_id=station_id).values_list("station_code",flat=True)
        if not trans_query:
            return APIResponse(0,'the data in the database is empty')
        trans_list = list(trans_query)
        trans_list.remove(station_id)
        station_code = trans_list[0]
        trans_data_list = []
        for res in res_list:
            dic = {
                "line_id": station_code[:2],
                "station_id": station_code,
                "global_code": str(global_code),
                "dir": "1",
                "up_number": up_number,
                "down_number": down_number,
                "arrive_load_rate": arrive_load_rate,
                'scheme_id': scheme_id,
            }
            dic.update(res)
            dic2 = {
                "line_id": station_code[:2],
                "station_id": station_code,
                "global_code": str(global_code),
                "dir": "2",
                "up_number": up_number,
                "down_number": down_number,
                "arrive_load_rate": arrive_load_rate,
                'scheme_id': scheme_id,
            }
            dic2.update(res)
            trans_data_list.append(dic)
            trans_data_list.append(dic2)
            global_code += 1
        for data_dic in trans_data_list:
            models.TrainData.objects.create(**data_dic)

        return APIResponse(1,"数据预设完成")

class PsImport(APIView):
    # 客流数据模板下载
    def get(self,request,*args,**kwargs):
        # the_file_name = os.path.join(MEDIA_ROOT,"download","行车数据模板.xlsx")  # 要下载的文件路径
        # response = StreamingHttpResponse(common.file_iterator(the_file_name))  # 这里创建返回
        # response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        # response['Content-Disposition'] = 'attachment;filename="行车数据模板.xlsx"'  # 注意filename 这个是下载后的名字
        the_file_name = "media/download/客流数据模板.xlsx"
        res = DOWNLOAD + the_file_name
        return APIResponse(results=res)

    # 客流数据excel导入
    def post(self,request,*args,**kwargs):
        # 换乘车站  非换乘车站
        station_type = request.data.get('station_type')
        scheme_id = request.data.get('scheme_id')
        station_id = request.data.get('station_id')
        file_obj = request.data.get('file')
        if not (station_type and scheme_id and station_type and station_id and file_obj):
            return APIResponse(0,'the data_type is empty')
        if station_type not in ["换乘车站",'非换乘车站']:
            return APIResponse(0,'the station_type is error')

        def read_inout_excel():
            """读取excel文件"""
            data_list = []
            book = xlrd.open_workbook(filename=file_obj.name, file_contents=file_obj.read())

            # 获取索引为3的sheet
            sheet0 = book.sheet_by_index(0)
            # 获取所有的行
            nrows = sheet0.nrows
            # 获取第3行到最后一行数据
            for i in range(2, nrows):
                row_data = sheet0.row_values(i)
                date = str(datetime.datetime.now().date())
                data_dic = {
                    "scheme_id": scheme_id,
                    "station_id":station_id,
                    "line_id": LINE_DIC.get(row_data[1]),
                    "dir": "01" if row_data[2] == "上行" else "02",
                    "stat_tm": date+" "+row_data[3],
                    "entry_quantity": int(row_data[4]),
                    "exit_quantity": int(row_data[5]),
                }
                data_list.append(data_dic)
            return data_list
        res = read_inout_excel()
        for data_dic in res:
            # 2020年6月12日 14:15:00
            # print(data_dic)
            try:
                models.FlowInOutDetail.objects.create(**data_dic)
            except Exception as e:
                print(e)
        if station_type == "非换乘车站":
            return APIResponse(1,'in out flow save into database')

        def read_trans_excel():
            """读取excel文件"""
            data_list = []
            book = xlrd.open_workbook(filename=file_obj.name, file_contents=file_obj.read())

            # 获取索引为3的sheet
            sheet1 = book.sheet_by_index(1)
            # 获取所有的行
            nrows = sheet1.nrows
            # 获取第2行到最后一行数据
            for i in range(2, nrows):
                row_data = sheet1.row_values(i)
                date = str(datetime.datetime.now().date())
                data_dic = {
                    "scheme_id": scheme_id,
                    "station_id":station_id,
                    "from_line_id":LINE_DIC.get(row_data[1]),
                    "to_line_id": LINE_DIC.get(row_data[3]),
                    "from_drct_cd": "01" if row_data[2] == "上行" else "02",
                    "to_drct_cd": "01" if row_data[2] == "上行" else "02",
                    "stat_tm": date + " "+ row_data[5],
                    "quantity": int(row_data[6]),
                }
                data_list.append(data_dic)
            return data_list

        res = read_trans_excel()

        for data_dic in res:
            # 2020年6月12日 14:15:00
            try:
                models.FlowTranDetail.objects.create(**data_dic)

            except Exception as e:
                print(e)
        return APIResponse(1, 'in out and trans flow save into database')

class DrImport(APIView):
    # 行车数据模板下载
    def get(self,request,*args,**kwargs):
        # the_file_name = os.path.join(MEDIA_ROOT,"download","行车数据模板.xlsx")  # 要下载的文件路径
        # response = StreamingHttpResponse(common.file_iterator(the_file_name))  # 这里创建返回
        # response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
        # response['Content-Disposition'] = 'attachment;filename="行车数据模板.xlsx"'  # 注意filename 这个是下载后的名字
        # # the_file_name = "media/download/行车数据模板.xlsx"
        # # res = DOWNLOAD + the_file_name
        # # return APIResponse(results=res)
        # return response
        the_file_name = "media/download/行车数据模板.xlsx"
        res = DOWNLOAD + the_file_name
        return APIResponse(results=res)
    # 行车数据数据excel导入
    def post(self,request,*args,**kwargs):
        # 换乘车站  非换乘车站
        station_type = request.data.get('station_type')
        scheme_id = request.data.get('scheme_id')
        station_id = request.data.get('station_id')
        file_obj = request.FILES.get('file')
        if not (station_type and scheme_id and station_type and file_obj):
            return APIResponse(0,'the data_type is empty')
        if station_type not in ["换乘车站",'非换乘车站']:
            return APIResponse(0,'the station_type is error')

        # 获取文件名称
        # name = file_obj.name
        # # 获取文件大小
        # size = file_obj.size
        data_list = []
        book = xlrd.open_workbook(filename=file_obj.name, file_contents=file_obj.read())  # 关键点在于这里
        # 获取索引为0的sheet
        sheet0 = book.sheet_by_index(0)
        # 获取所有的行
        nrows = sheet0.nrows
        # 获取第3行到最后一行数据
        for i in range(2, nrows):
            row_data = sheet0.row_values(i)
            line_id = LINE_DIC.get(row_data[1])
            date = datetime.datetime.now().date()
            arrive_time = str(date) +" "+str(row_data[4])
            depart_time = str(date) +" "+str(row_data[5])
            ride_time = datetime.datetime.strptime(depart_time,"%Y-%m-%d %X") - datetime.datetime.strptime(arrive_time,"%Y-%m-%d %X")
            if station_type == "非换乘车站":
                data_dic = {
                    "line_id":line_id,
                    "station_id":station_id,
                    "global_code":str(row_data[2]),
                    "dir":"1" if row_data[3]=="上行" else '2',
                    "arrive_time":arrive_time,
                    "depart_time":depart_time,
                    "ride_time":int(ride_time.seconds),
                    "up_number":int(row_data[6]),
                    "down_number":int(row_data[7]),
                    "arrive_load_rate":float(row_data[8]),
                    'scheme_id':scheme_id,
                }
                data_list.append(data_dic)
            else:
                station_code = TransStation.objects.filter(station_id=station_id).values_list(
                    "station_code").exclude(station_code=station_id).first().station_code
                if not station_code:
                    return APIResponse(0,'station_code is null')

                data_dic = {
                    "line_id": line_id,
                    "station_id": station_id if line_id == station_id[:2] else station_code,
                    "global_code": str(row_data[2]),
                    "dir": "1" if row_data[3] == "上行" else '2',
                    "arrive_time": arrive_time,
                    "depart_time": depart_time,
                    "ride_time": int(ride_time.seconds),
                    "up_number": int(row_data[6]),
                    "down_number": int(row_data[7]),
                    "arrive_load_rate": float(row_data[8]),
                    'scheme_id': scheme_id,
                }
                data_list.append(data_dic)

        for data_dic in data_list:
            # 2020年6月12日 14:15:00
            # print(data_dic)
            try:
                models.TrainData.objects.create(**data_dic)
            except Exception as e:
                print(e)
        return APIResponse(1,'driving data save into database')







# def file_down(request, id):
#     """
#     下载压缩文件
#     :param request:
#     :param id: 数据库id
#     :return:
#     """
#     data = [{"id": "1", "image": "animation.jpg"}]  # 模拟mysql表数据
#     file_name = ""  # 文件名
#     for i in data:
#         if i["id"] == id:  # 判断id一致时
#             file_name = i["image"]  # 覆盖变量
#
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
#     file_path = os.path.join(base_dir, 'upload', 'images', file_name)  # 下载文件的绝对路径
#
#     if not os.path.isfile(file_path):  # 判断下载文件是否存在
#         return HttpResponse("Sorry but Not Found the File")
#
#     def file_iterator(file_path, chunk_size=512):
#         """
#         文件生成器,防止文件过大，导致内存溢出
#         :param file_path: 文件绝对路径
#         :param chunk_size: 块大小
#         :return: 生成器
#         """
#         with open(file_path, mode='rb') as f:
#             while True:
#                 c = f.read(chunk_size)
#                 if c:
#                     yield c
#                 else:
#                     break
#
#     try:
#         # 设置响应头
#         # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
#         response = StreamingHttpResponse(file_iterator(file_path))
#         # 以流的形式下载文件,这样可以实现任意格式的文件下载
#         response['Content-Type'] = 'application/octet-stream'
#         # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
#         response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
#     except:
#         return HttpResponse("Sorry but Not Found the File")
#
#     return response





# def downloadTest(request):
#     the_file_name ="D:\test.xls"#要下载的文件路径
#     response =StreamingHttpResponse(file_iterator(the_file_name))#这里创建返回
#     response['Content-Type'] = 'application/vnd.ms-excel'#注意格式
#     response['Content-Disposition'] = 'attachment;filename="模板.xls"'#注意filename 这个是下载后的名字
#     return response
#这里选用了StreamingHttpResponse返回,还有其他的方式，请查看下面的url

class PassFlow(APIView):
    """进出站客流数据展示"""
    def get(self,request,*args,**kwargs):
        # 获取方案id
        scheme_id = request.query_params.get('scheme_id')
        # 获取车站类型
        station_type = request.query_params.get('station_type')
        # 获取车站id
        station_id = request.query_params.get('station_id')
        if not (scheme_id and station_type and station_id):
            return APIResponse(0,'the param is None')
        if station_type not in ['非换乘车站','换乘车站']:
            return APIResponse(0,'station_type is error')

        inout_query = models.FlowInOutDetail.objects.filter(scheme_id=scheme_id).all()
        if not inout_query:
            return APIResponse(0,'the data in the database is null')
        inout_data = serializers.FlowInOutDetailSerializer(inout_query,many=True).data

        if station_type == "非换乘车站":
            line_list = [station_id[0:2],"全部线路"]
            return APIResponse(in_data=inout_data,out_data=inout_data,line_data=line_list)

        trans_query = models.FlowTranDetail.objects.filter(scheme_id=scheme_id).all()
        if not trans_query:
            return APIResponse(0,'the data in the database is null')

        line_query = TransStation.objects.filter(station_id=station_id).values_list("line_id", flat=True)
        if not line_query:
            return APIResponse(0, 'the data in the database is null')
        line_data = list(line_query)
        line_data.append("全部线路")
        trans_data = serializers.FlowTranDetailSerializer(trans_query,many=True).data
        return APIResponse(2,in_data=inout_data,out_data=inout_data,trans_data=trans_data,line_data=line_data)
    # 对进出站、换乘客流数据进行局部修改 修改后的数据用于作为仿真数据
    def patch(self,request,*args,**kwargs):
        category = request.data.get('type')
        request_data = request.data.get('pager_flow')
        if not (request_data and category):
            return APIResponse(0, 'the param is null')

        if category not in [1,2]:
            return APIResponse(0,'the station_type is error')
        pk = request_data.get('id')
        if category == 1:
            flow_query = models.FlowInOutDetail.objects.filter(pk=pk).first()

            flow_ser = serializers.FlowInOutDetailSerializer(instance=flow_query, data=request_data, partial=True)
            flow_ser.is_valid(raise_exception=True)
            flow_obj = flow_ser.save()
            results = serializers.FlowInOutDetailSerializer(flow_obj).data
            return APIResponse(results=results)
        tran_query = models.FlowTranDetail.objects.filter(pk=pk).first()
        tran_ser = serializers.FlowTranDetailSerializer(instance=tran_query, data=request_data, partial=True)
        tran_ser.is_valid(raise_exception=True)
        tran_obj = tran_ser.save()
        results = serializers.FlowTranDetailSerializer(tran_obj).data
        return APIResponse(results=results)

class Driving(APIView):
    def get(self,request,*args,**kwargs):
        # 获取方案id
        scheme_id = request.query_params.get('scheme_id')
        if not scheme_id:
            return APIResponse(0,'the param maybe be not enough')

        queryset = models.TrainData.objects.filter(scheme_id=scheme_id).all()
        if not queryset:
            return APIResponse(0,"the data on the database not exist")
        query_data = serializers.TrainDataSerializer(queryset,many=True).data
        return APIResponse(results=query_data)

    def post(self,request,*args,**kwargs):
        pass

    def patch(self,request,*args,**kwargs):
        request_data = request.data.get('driving_data')
        if not request_data:
            return APIResponse(0,'the param maybe not enough')

        pk = request_data.get('id')
        train_query = models.TrainData.objects.filter(pk=pk).first()

        train_ser = serializers.TrainDataSerializer(instance=train_query, data=request_data, partial=True)
        train_ser.is_valid(raise_exception=True)
        train_obj = train_ser.save()
        results = serializers.TrainDataSerializer(train_obj).data
        return APIResponse(results=results)

class SimationAPIView(APIView):
    def post(self,request,*args,**kwargs):
        scheme_id = request.data.get("scheme_id")
        back_dic = {
            "status": 0,
            "msg": "",
        }
        if scheme_id is None:
            back_dic['msg'] = "方案id不存在"
            return JsonResponse(back_dic,safe=False,json_dumps_params={'ensure_ascii':False})
        scheme_obj = TrainScheme.objects.filter(scheme_id=scheme_id).first()
        if not scheme_obj:
            back_dic['msg'] = "方案不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        StartTime = scheme_obj.psflow_date +" "+scheme_obj.start_time
        EndTime = scheme_obj.psflow_date+" "+scheme_obj.end_time
        # 进出站数据
        query = models.FlowInOutDetail.objects.filter(scheme_id=scheme_id).all()
        if not query:
            back_dic['msg'] = "进出站数据不存在"
            return JsonResponse(back_dic,safe=False,json_dumps_params={'ensure_ascii':False})

        # 进站客流数据
        query_in_data = serializers.FlowInDetailSerializer(query,many=True).data
        AccinParams = query_in_data

        # 出站客流数据
        query_out_data = serializers.FlowOutDetailSerializer(query,many=True).data
        AccoutParams = query_out_data

        # 换乘客流数据
        tran_query = models.FlowTranDetail.objects.filter(scheme_id=scheme_id).all()

        if not tran_query:
            back_dic['msg'] = "换乘数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        # 换乘客流数据
        tran_query_data = serializers.FlowTranDetailSerializer(tran_query,many=True).data
        AccTransParams = tran_query_data
        # 行车数据
        driving_query = models.TrainData.objects.filter(scheme_id=scheme_id).all()
        if not driving_query:
            back_dic['msg'] = "行车数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        driving_data = serializers.TrainDataSerializer(driving_query, many=True).data
        TrainParams = driving_data

        # 固定数据
        Per_time_unit = 900
        isInsertDB = True
        isInsert3D_DB = False

        comp_obj = models.EmuPsComp.objects.filter(scheme_id=scheme_id).first()
        if not comp_obj:
            back_dic['msg'] = "乘客数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        pParam = serializers.pParamSerializer(comp_obj).data
        equ_obj = models.EmuPsEquipment.objects.filter(scheme_id=scheme_id).first()
        if not equ_obj:
            back_dic['msg'] = "设备使用数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        eParam = serializers.eParamSerializer(equ_obj).data
        gate_obj = models.EmuGateStatus.objects.filter(scheme_id=scheme_id).all()
        es_obj = models.EmuEsCsStatus.objects.filter(scheme_id=scheme_id).all()
        fen_obj = models.EmuFenceStatus.objects.filter(scheme_id=scheme_id).all()
        way_obj = models.EmuGateWayStatus.objects.filter(scheme_id=scheme_id).all()
        if not (gate_obj and es_obj and fen_obj and way_obj):
            back_dic['msg'] = "客运组织数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        gate_data = serializers.GaSerializer(gate_obj,many=True).data
        es_data = serializers.EsSerializer(es_obj,many=True).data
        fen_data = serializers.FenSerializer(fen_obj,many=True).data
        way_data = serializers.GaSerializer(way_obj,many=True).data
        gate_data.extend(es_data)
        gate_data.extend(fen_data)
        gate_data.extend(way_data)

        in_out_query = models.EmuInOutRate.objects.filter(scheme_id=scheme_id).all()
        part_query = models.EmuTrainPartRate.objects.filter(scheme_id=scheme_id).all()
        if not (in_out_query and part_query):
            back_dic['msg'] = "进出口,车厢上下车数据不存在"
            return JsonResponse(back_dic, safe=False, json_dumps_params={'ensure_ascii': False})
        in_out_data = serializers.InOutSerializer(in_out_query,many=True).data
        part_data = serializers.PartSerializer(part_query,many=True).data
        in_out_data.extend(part_data)
        runParams = [
            {
                # 方案id
                "senceId": scheme_id,
                # 乘客基本表
                "pParam": pParam,
                # 设备使用信息表
                "eParam": eParam,
                # 客运数据表
                "eStaus": gate_data,
                # 出入口,车厢表
                "eRate": in_out_data
            }
        ]
        json_data = {
            "Sheme_id":scheme_id,
            "StartTime":StartTime,
            "EndTime":EndTime,

            "Per_time_unit":Per_time_unit,
            "isInsertDB":isInsertDB,
            "isInsert3D_DB":isInsert3D_DB,
            "runParams":runParams,
            "AccinParams":AccinParams,
            "AccoutParams":AccoutParams,
            "AccTransParams":AccTransParams,
            "TrainParams":TrainParams,
        }
        return JsonResponse(json_data,safe=False)
"""
{
  "msgHead":{
    "msgId": 6,  // 数据标识
    "sendTime": "2019-11-06 11-38-29"
  },
  
  "msgBody":[
    {
      "Index": "2020-04-17 17:40:25",
      "PedID": "121",
      "SexType": 0,
      "AgeType": 1,
      "BagType": 1,
      "PositionX": 34.522,
      "PositionY": 16.271,
      "PedState": 1,
      "LayerID": "L021002",
      "EquipID": "E0101"
    }
    ]
}
"""
# from station_info.models import TrainScheme
# class SimAPIView(APIView):
#     def post(self,request,*args,**kwargs):
#         Sid = request.data.get('sceneId')
#         Index = request.data.get('dateTime')
#         PersonInfo = request.data.get('personInfo')
#         if not (Sid and Index and PersonInfo):
#             return APIResponse(0,'sceneId is empty')
#         sendTime = str(datetime.datetime.now())
#         TrainScheme.objects.filter(scheme_id=Sid)
#         msgHead_dict = {}
#         msg_list = []
#         for info in PersonInfo:
#             info["Index"] = Index
#             msg_dic = {
#                 'msgHead':msgHead_dict,
#                 "msgBody":info,
#             }
#             msg_list.append(msg_dic)
#
#
#
#
#         producer = KafkaProducer(bootstrap_servers=list)
#         for send_msg in msg_list:
#             msg = json.dumps(send_msg)
#             producer.send('LINE10_ATS', msg, partition=0)
#         print("send msg")
#         # time.sleep(1)
#
#         producer.close()
#
#         return APIResponse(0,'ok')

class SimulationOutputAPIView(APIView):
    """模型输出数据"""
    def post(self,request,*args,**kwargs):
        # 获取模型输出信息
        sqlstr = request.data.get('sqlstr')
        if not sqlstr:
            return APIResponse(0,'the sqlstr is empty')
        sql_list = sqlstr.split(";")
        for sql in sql_list:
            if not sql:
                continue
            try:
                cursor.execute(sql)
            except Exception as e:
                print(e)
            # 写入日志查看
            logger.info("get data: %s" % (sql))
        return APIResponse(1, 'ok')

class EmuGateStatusAPIView(ListAPIView):
    """闸机"""
    queryset = models.EmuGateStatus.objects.all()
    serializer_class = serializers.EmuGateStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id','ps_pare_type','scheme_id']

    def get(self,request,*args,**kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            gate_obj = GateStatus.objects.filter(station_id=request.query_params.get('station_id'),ps_pare_type=request.query_params.get('ps_pare_type')).all()
            gate_list = []
            if not gate_obj:
                return APIResponse(0,'the basic databses is null')
            for gate in gate_obj:
                gate_dic = {
                    "scheme_id":request.query_params.get('scheme_id'),
                    "station_id":gate.station_id,
                    "ps_pare_type":gate.ps_pare_type,
                    "loc":gate.loc,
                    "eq_id":gate.eq_id,
                    "equ_name":gate.equ_name,
                    "eq_status":gate.eq_status,
                }
                gate_list.append(gate_dic)
            data_list = []
            for gate_dic in gate_list:
                gate_obj = models.EmuGateStatus.objects.create(**gate_dic)
                gate_ser = serializers.EmuGateStatusSerializer(gate_obj).data
                data_list.append(gate_ser)

            return APIResponse(results=data_list)

        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_gate_obj = models.EmuGateStatus.objects.filter(pk=pk).first()

        gate_ser = serializers.EmuGateStatusSerializer(instance=old_gate_obj, data=request_data, partial=True)
        gate_ser.is_valid(raise_exception=True)
        gate_obj = gate_ser.save()
        results = serializers.EmuGateStatusSerializer(gate_obj).data
        return APIResponse(results=results)

class EmuEsCsStatusAPIView(ListAPIView):
    """扶梯"""
    queryset = models.EmuEsCsStatus.objects.all()
    serializer_class = serializers.EmuEsCsStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type','scheme_id']

    def get(self,request,*args,**kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            cs_obj = EsCsStatus.objects.filter(station_id=request.query_params.get('station_id'),ps_pare_type=request.query_params.get('ps_pare_type')).all()
            cs_list = []
            if not cs_obj:
                return APIResponse(0,'the basic databses is null')
            for cs in cs_obj:
                cs_dic = {
                    "scheme_id":request.query_params.get('scheme_id'),
                    "station_id":cs.station_id,
                    "ps_pare_type":cs.ps_pare_type,
                    "loc":cs.loc,
                    "eq_id": cs.eq_id,
                    "equ_name":cs.equ_name,
                    "eq_status":cs.eq_status,
                }
                cs_list.append(cs_dic)
            data_list = []
            for cs_dic in cs_list:
                cs_obj = models.EmuEsCsStatus.objects.create(**cs_dic)
                cs_ser = serializers.EmuEsCsStatusSerializer(cs_obj).data
                data_list.append(cs_ser)

            return APIResponse(results=data_list)

        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_es_obj = models.EmuEsCsStatus.objects.filter(pk=pk).first()

        es_ser = serializers.EmuEsCsStatusSerializer(instance=old_es_obj, data=request_data, partial=True)
        es_ser.is_valid(raise_exception=True)
        es_obj = es_ser.save()
        results = serializers.EmuEsCsStatusSerializer(es_obj).data
        return APIResponse(results=results)

class EmuFenceStatusAPIView(ListAPIView):
    """导流栏"""
    queryset = models.EmuFenceStatus.objects.all()
    serializer_class = serializers.EmuFenceStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type','scheme_id']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            fen_obj = FenceStatus.objects.filter(station_id=request.query_params.get('station_id'),
                                               ps_pare_type=request.query_params.get('ps_pare_type')).all()
            fen_list = []
            if not fen_obj:
                return APIResponse(0, 'the basic databses is null')
            for fen in fen_obj:
                fen_dic = {
                    "scheme_id": request.query_params.get('scheme_id'),
                    "station_id": fen.station_id,
                    "ps_pare_type": fen.ps_pare_type,
                    "loc": fen.loc,
                    "eq_id": fen.eq_id,
                    "equ_name": fen.equ_name,
                    "eq_status": fen.eq_status,
                }
                fen_list.append(fen_dic)
            data_list = []
            for fen_dic in fen_list:
                fen_obj = models.EmuFenceStatus.objects.create(**fen_dic)
                fen_ser = serializers.EmuFenceStatusSerializer(fen_obj).data
                data_list.append(fen_ser)

            return APIResponse(results=data_list)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_fen_obj = models.EmuFenceStatus.objects.filter(pk=pk).first()

        fen_ser = serializers.EmuFenceStatusSerializer(instance=old_fen_obj, data=request_data, partial=True)
        fen_ser.is_valid(raise_exception=True)
        fen_obj = fen_ser.save()
        results = serializers.EmuFenceStatusSerializer(fen_obj).data
        return APIResponse(results=results)

class EmuGateWayStatusAPIView(ListAPIView):
    """出入口"""
    queryset = models.EmuGateWayStatus.objects.all()
    serializer_class = serializers.EmuGateWayStatusSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id', 'ps_pare_type','scheme_id']

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        if not response.data:
            way_obj = GateWayStatus.objects.filter(station_id=request.query_params.get('station_id'),
                                                 ps_pare_type=request.query_params.get('ps_pare_type')).all()
            way_list = []
            if not way_obj:
                return APIResponse(0, 'the basic databses is null')
            for way in way_obj:
                way_dic = {
                    "scheme_id": request.query_params.get('scheme_id'),
                    "station_id": way.station_id,
                    "ps_pare_type": way.ps_pare_type,
                    "loc": way.loc,
                    "eq_id": way.eq_id,
                    "equ_name": way.equ_name,
                    "orig_in_rate":way.orig_in_rate,
                    "var_in_rate":way.var_in_rate,
                    "orig_out_rate":way.orig_out_rate,
                    "var_out_rate":way.var_out_rate,
                    "eq_status": way.eq_status,
                }
                way_list.append(way_dic)
            data_list = []
            for way_dic in way_list:
                way_obj = models.EmuGateWayStatus.objects.create(**way_dic)
                way_ser = serializers.EmuGateWayStatusSerializer(way_obj).data
                data_list.append(way_ser)

            return APIResponse(results=data_list)
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        way_list = request.data.get('way_list')
        if not way_list:
            return APIResponse(0,'way_list is empty')
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
                obj = models.EmuGateWayStatus.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(way_list[index])
            except Exception as e:
                print(e)
                continue
        # 多条数据整体改
        way_ser = serializers.EmuGateWayStatusSerializer(instance=objs, data=new_request_data, partial=False, many=True)
        way_ser.is_valid(raise_exception=True)
        way_objs = way_ser.save()
        results = serializers.EmuGateWayStatusSerializer(way_objs, many=True).data
        return APIResponse(results=results)

class EmuPsCompAPIView(APIView):
    """乘客基本属性"""
    def get(self,request,*args,**kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')
        scheme_id = request.query_params.get('scheme_id')
        if not (station_id and ps_pare_type and scheme_id):
            return APIResponse(0,'maybe only having a param is null')

        response = models.EmuPsComp.objects.filter(station_id=station_id,ps_pare_type=ps_pare_type,scheme_id=scheme_id).first()
        if response:
            ps_data = serializers.EmuPsCompSerializer(response).data
            return APIResponse(results=ps_data)

        ps_obj = PsComp.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type).first()
        if not ps_obj:
            return APIResponse(0, 'the data in the database is empty')

        ps_dic = {
            "scheme_id": scheme_id,
            "station_id": ps_obj.station_id,
            "ps_pare_type": ps_obj.ps_pare_type,
            "male_rate": ps_obj.male_rate,
            "female_rate":ps_obj.female_rate,
            "personal_rate":ps_obj.personal_rate,
            "team_rate": ps_obj.team_rate,
            "older_rate": ps_obj.older_rate,
            "adult_rate": ps_obj.adult_rate,
            "child_rate": ps_obj.child_rate,
            "no_bag_rate": ps_obj.no_bag_rate,
            "small_bag_rate": ps_obj.small_bag_rate,
            "big_bag_rate": ps_obj.big_bag_rate,

            "mo_speed": ps_obj.mo_speed,
            "mo_space": ps_obj.mo_space,
            "ma_speed": ps_obj.ma_speed,
            "ma_space": ps_obj.ma_space,
            "mc_speed": ps_obj.mc_speed,
            "mc_space": ps_obj.mc_space,

            "fo_speed": ps_obj.fo_speed,
            "fo_space": ps_obj.fo_space,
            "fa_speed": ps_obj.fa_speed,
            "fa_space": ps_obj.fa_space,
            "fc_speed": ps_obj.fc_speed,
            "fc_space": ps_obj.fc_space,
        }

        emps_obj = models.EmuPsComp.objects.create(**ps_dic)
        ps_data = serializers.EmuPsCompSerializer(emps_obj).data
        return APIResponse(results=ps_data)


    # 单条数据的全部修改
    def put(self,request,*args,**kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0,'the param is null')

        pk = request_data.get('id')
        old_ps_obj = models.EmuPsComp.objects.filter(pk=pk).first()

        ps_ser = serializers.EmuPsCompSerializer(instance=old_ps_obj, data=request_data, partial=False)
        ps_ser.is_valid(raise_exception=True)
        ps_obj = ps_ser.save()
        results = serializers.EmuPsCompSerializer(ps_obj).data
        return APIResponse(results=results)

class EmuPsEquipmentAPIView(APIView):
    """设备使用信息"""

    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')
        scheme_id = request.query_params.get('scheme_id')

        if not (station_id and ps_pare_type and scheme_id):
            return APIResponse(0, 'maybe only having a param is null')

        response = models.EmuPsEquipment.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type,scheme_id=scheme_id).first()
        if response:
            equ_data = serializers.EmuPsEquipmentSerializer(response).data
            return APIResponse(results=equ_data)

        equ_obj = PsEquipment.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type).first()
        if not equ_obj:
            return APIResponse(0, 'the data in the database is empty')

        equ_dic = {
            "scheme_id": scheme_id,
            "station_id": equ_obj.station_id,
            "ps_pare_type": equ_obj.ps_pare_type,
            "is_transfer": equ_obj.is_transfer,
            "no_use_rate": equ_obj.no_use_rate,
            "sc_big_bag_time": equ_obj.sc_big_bag_time,
            "sc_small_bag_time": equ_obj.sc_small_bag_time,
            "sc_fast_time": equ_obj.sc_fast_time,
            "sc_fast_rate": equ_obj.sc_fast_rate,
            "tvm_use_rate": equ_obj.tvm_use_rate,
            "tvm_tickets_rate": equ_obj.tvm_tickets_rate,
            "tvm_tickets_time": equ_obj.tvm_tickets_time,
            "tvm_recharge_rate": equ_obj.tvm_recharge_rate,
            "tvm_recharge_time": equ_obj.tvm_recharge_time,
            "bom_use_rate": equ_obj.bom_use_rate,

            "bom_tickets_rate": equ_obj.bom_tickets_rate,
            "bom_tickets_time": equ_obj.bom_tickets_time,
            "bom_recharge_rate": equ_obj.bom_recharge_rate,
            "bom_recharge_time": equ_obj.bom_recharge_time,
            "gate_normal_time": equ_obj.gate_normal_time,
            "gate_big_bag_time": equ_obj.gate_big_bag_time,
        }

        emequ_obj = models.EmuPsEquipment.objects.create(**equ_dic)
        emequ_data = serializers.EmuPsEquipmentSerializer(emequ_obj).data
        return APIResponse(results=emequ_data)

    # 单条数据的全部修改
    def put(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_equ_obj = models.EmuPsEquipment.objects.filter(pk=pk).first()

        equ_ser = serializers.EmuPsEquipmentSerializer(instance=old_equ_obj, data=request_data, partial=False)
        equ_ser.is_valid(raise_exception=True)
        equ_obj = equ_ser.save()
        results = serializers.EmuPsEquipmentSerializer(equ_obj).data
        return APIResponse(results=results)

class EmuPsFacilitiesAPIView(APIView):
    """设备设施能力"""
    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')
        scheme_id = request.query_params.get('scheme_id')

        if not (station_id and ps_pare_type and scheme_id):
            return APIResponse(0, 'maybe only having a param is null')

        response = models.EmuPsFacilities.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type,scheme_id=scheme_id).first()
        if response:
            fac_data = serializers.EmuPsFacilitiesSerializer(response).data
            return APIResponse(results=fac_data)

        fac_obj = PsFacilities.objects.filter(station_id=station_id, ps_pare_type=ps_pare_type).first()
        if not fac_obj:
            return APIResponse(0, 'the data in the database is empty')

        fac_dic = {
            "scheme_id": scheme_id,
            "station_id": fac_obj.station_id,
            "ps_pare_type": fac_obj.ps_pare_type,
            "is_transfer": fac_obj.is_transfer,
            "stup_design_cap": fac_obj.stup_design_cap,
            "stdown_design_cap": fac_obj.stdown_design_cap,
            "stmix_design_cap": fac_obj.stmix_design_cap,
            "esup_design_cap": fac_obj.esup_design_cap,
            "esdown_design_cap": fac_obj.esdown_design_cap,
            "la_design_cap": fac_obj.la_design_cap,
            "el_design_cap": fac_obj.el_design_cap,
            "thsin_design_cap": fac_obj.thsin_design_cap,
            "thdou_design_cap": fac_obj.thdou_design_cap,
            "gasin_design_cap": fac_obj.gasin_design_cap,

            "gadou_design_cap": fac_obj.gadou_design_cap,
            "sc_design_cap": fac_obj.sc_design_cap,
        }

        emefac_obj = models.EmuPsFacilities.objects.create(**fac_dic)
        emufac_data = serializers.EmuPsFacilitiesSerializer(emefac_obj).data
        return APIResponse(results=emufac_data)
    # 单条数据的全部修改
    def put(self, request, *args, **kwargs):
        request_data = request.data
        if not request_data:
            return APIResponse(0, 'the param is null')

        pk = request_data.get('id')
        old_fac_obj = models.EmuPsFacilities.objects.filter(pk=pk).first()

        fac_ser = serializers.EmuPsFacilitiesSerializer(instance=old_fac_obj, data=request_data, partial=False)
        fac_ser.is_valid(raise_exception=True)
        fac_obj = fac_ser.save()
        results = serializers.EmuPsFacilitiesSerializer(fac_obj).data
        return APIResponse(results=results)

class EmuInOutRateAPIView(APIView):
    """出入口比例"""
    def get(self, request, *args, **kwargs):
        station_id = request.query_params.get('station_id')
        ps_pare_type = request.query_params.get('ps_pare_type')
        scheme_id = request.query_params.get('scheme_id')
        if not (station_id and ps_pare_type and scheme_id):
            return APIResponse(0, 'The params is null')

        inout_query = models.EmuInOutRate.objects.filter(
            station_id=station_id,
            ps_pare_type=ps_pare_type,
            scheme_id=scheme_id
        ).all()

        if inout_query:
            inout_data = serializers.EmuInOutRateSerializer(inout_query, many=True).data

            return APIResponse(in_data=inout_data, out_data=inout_data)
        # 数据库表中没有数据走这个 从模板数据库中获取数据
        inout_queryset = InOutRate.objects.filter(
            station_id=station_id,
            ps_pare_type=ps_pare_type,
        ).all()

        if not inout_queryset:
            return APIResponse(0, 'the data in the database is empty')
        # in_queryset = inout_queryset.filter(in_out_type='进站').all()
        # out_queryset = inout_queryset.filter(in_out_type='出站').all()
        in_out_list = []
        for inout_query in inout_queryset:
            inout_dic = {
                "station_id": inout_query.station_id,
                "ps_pare_type":inout_query.ps_pare_type,
                "eq_id":inout_query.eq_id,
                "in_rate":inout_query.in_rate,
                "out_rate":inout_query.out_rate,
                "scheme_id":scheme_id
            }
            in_out_list.append(inout_dic)
        in_out_data_list = []
        for in_out_dic in in_out_list:
            in_out_obj = models.EmuInOutRate.objects.create(**in_out_dic)
            in_out_ser = serializers.EmuInOutRateSerializer(in_out_obj).data
            in_out_data_list.append(in_out_ser)

        return APIResponse(in_data=in_out_data_list, out_data=in_out_data_list)

    def put(self, request, *args, **kwargs):
        ent_list = request.data.get('ent_list')
        if not ent_list:
            return APIResponse(0,'ent_list is empty')
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
                obj = models.EmuInOutRate.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(ent_list[index])
            except Exception as e:
                print(e)
                continue
        # 多条数据整体修改
        ent_ser = serializers.EmuInOutRateSerializer(instance=objs, data=new_request_data, partial=False, many=True)
        ent_ser.is_valid(raise_exception=True)
        ent_objs = ent_ser.save()
        results = serializers.EmuInOutRateSerializer(ent_objs, many=True).data
        return APIResponse(results=results)

class EmuTrainPartRateAPIView(APIView):
    """车厢选择比例"""
    def get(self, request, *args, **kwargs):
        # 这个是换乘站的标识
        station_type = request.query_params.get('station_type')
        # 车站的编码
        station_id = request.query_params.get('station_id')
        # 峰值类型
        ps_pare_type = request.query_params.get('ps_pare_type')
        # 方案id
        scheme_id = request.query_params.get('scheme_id')
        if not (station_id and ps_pare_type and station_type and scheme_id):
            return APIResponse(0,'The params is null')

        if station_type not in ["换乘车站",'非换乘车站']:
            return APIResponse(0,'station_type is false')

        if station_type == '非换乘车站':
            up_query = models.EmuTrainPartRate.objects.filter(station_id=station_id,scheme_id=scheme_id ,ps_pare_type=ps_pare_type,direct_id="上行").all()
            if up_query:

                down_query = models.EmuTrainPartRate.objects.filter(station_id=station_id,scheme_id=scheme_id,ps_pare_type=ps_pare_type,direct_id="下行").all()

                up_data = serializers.EmuTrainPartRateSerializer(up_query, many=True).data
                down_data = serializers.EmuTrainPartRateSerializer(down_query, many=True).data

                return APIResponse(up_data=up_data, down_data=down_data)

            else:
                # 获取数据
                part_query = TrainPartRate.objects.filter(station_id=station_id,ps_pare_type=ps_pare_type).all()
                part_list = []
                for part in part_query:
                    part_dic = {
                        "scheme_id":scheme_id,
                        "station_id":part.station_id,
                        "ps_pare_type":part.ps_pare_type,
                        "direct_id":part.direct_id,
                        "line_name":part.line_name,
                        "eq_id":part.eq_id,
                        "board_rate":part.board_rate,
                        "getoff_rate":part.getoff_rate,
                    }
                    part_list.append(part_dic)
                data_list = []
                for part_dic in part_list:
                    part_obj = models.EmuTrainPartRate.objects.create(**part_dic)
                    part_ser = serializers.EmuTrainPartRateSerializer(part_obj).data
                    data_list.append(part_ser)

                up_data = [data for data in data_list if data.get('direct_id') == '上行']
                down_data = [data for data in data_list if data.get('direct_id') == '下行']
                return APIResponse(up_data=up_data, down_data=down_data)

        else:
            station_query = TransStation.objects.filter(station_id=station_id).values_list('station_code',flat=True)
            if not station_query:
                return APIResponse(0,'the data in the database is empty')
            station_list = list(station_query,)
            # 全部的数据
            emutra_query = models.EmuTrainPartRate.objects.filter(station_id__in=station_list,ps_pare_type=ps_pare_type,scheme_id=scheme_id).all()
            data_list = []
            if emutra_query:
                for emutra in emutra_query:
                    emutra_data = serializers.EmuTrainPartRateSerializer(emutra).data
                    data_list.append(emutra_data)

                return APIResponse(2,results=data_list)
            # 获取的是列表套字典的形式
            train_part = TrainPartRate.objects.filter(station_id__in=station_list, ps_pare_type=ps_pare_type).all()
            train_data_list = []
            for train_obj in train_part:
                train_dic = {
                    "scheme_id":scheme_id,
                    "station_id":train_obj.station_id,
                    "ps_pare_type":train_obj.ps_pare_type,
                    "direct_id":train_obj.direct_id,
                    "line_name":train_obj.line_name,
                    "eq_id":train_obj.eq_id,
                    "board_rate":train_obj.board_rate,
                    "getoff_rate":train_obj.getoff_rate,
                }
                train_data_list.append(train_dic)

            for train_dic in train_data_list:
                models.EmuTrainPartRate.objects.create(**train_dic)

            emutra_query = models.EmuTrainPartRate.objects.filter(station_id__in=station_list,ps_pare_type=ps_pare_type, scheme_id=scheme_id).all()
            for emutra in emutra_query:
                emutra_data = serializers.EmuTrainPartRateSerializer(emutra).data
                data_list.append(emutra_data)

            return APIResponse(2,results=data_list)

    def put(self, request, *args, **kwargs):
        part_list = request.data.get('part_list')
        if not part_list:
            return APIResponse(0,'part_list is empty')
        length = len(part_list)
        if not length:
            return APIResponse(0, 'part_list is None')
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
                obj = models.EmuTrainPartRate.objects.get(pk=pk)
                # 把要修改的对象追加到对象列表中
                objs.append(obj)
                # 对应索引的数据就需要保存下来
                new_request_data.append(part_list[index])
            except Exception as e:
                print(e)
                continue
        # 多条数据整体修改
        part_ser = serializers.EmuTrainPartRateSerializer(instance=objs, data=new_request_data, partial=False, many=True)
        part_ser.is_valid(raise_exception=True)
        part_objs = part_ser.save()
        results = serializers.EmuTrainPartRateSerializer(part_objs, many=True).data
        return APIResponse(results=results)













