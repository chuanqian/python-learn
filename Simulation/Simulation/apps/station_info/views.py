from utils.response import APIResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,DestroyAPIView,UpdateAPIView,ListAPIView, RetrieveUpdateAPIView,RetrieveAPIView
from . import models
from lib.models import TransStation
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
import time
import logging
from settings.dev import BASE_URL,FUNC_ID
logger = logging.getLogger('logger')
"""
创建方案接口：http://127.0.0.1:8000/opera/schemes/
get请求：
响应数据
post请求参数：
    {
        "scheme_id":"ID1234",         方案ID  string
        "line_id":"02",             车站线路  string
        "station_name": "狮子山站",   车站名  string
        "scheme_type":"正常方案",     方案类型 string
        "scheme_name": "方案1",           方案名称  string
        "create_by":"张三",         创建人   string
        "scheme_desc":"这是一个好方案"            方案描述  string
    }

"""
# /line/
class LineAPIView(ListAPIView):
    """展示某条线路下的所有车站"""
    queryset = models.TrainLine.objects.all()
    serializer_class = serializers.TrainLineSerializer
    def get(self, request, *args, **kwargs):
        data_list = self.list(request, *args, **kwargs)
        return APIResponse(results=data_list.data)
# /station/8/
class StationAPIView(RetrieveUpdateAPIView):
    """展示某个车站的信息"""
    queryset = models.TrainStation.objects.all()
    serializer_class = serializers.TrainStationSerializer
    def get(self, request, *args, **kwargs):
        station_id = kwargs.get('pk')
        station_obj = models.TrainStation.objects.filter(station_id=station_id).first()
        if not station_obj:
            return APIResponse(0,'the data in the database is exist')
        response = serializers.TrainStationSerializer(station_obj).data
        return APIResponse(results=response)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

# /models/
# /models/5/
class ModelVersionsAPIView(ListAPIView,DestroyAPIView):
    """车站管理的模型版本所有的操作"""
    queryset = models.ModelVersion.objects.all()
    serializer_class = serializers.ModelVersionSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id']
    # 群查
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)
    # 单增
    def post(self,request,*args,**kwargs):
        # <QueryDict: {'ver_num': ['v1.06'], 'station_id': ['0101'], 'version_des': ['这是第6个模型版本'], 'founder': ['admin'], 'model_url': [<TemporaryUploadedFile: LOG.rar (application/x-rar-compressed)>]}>
        request_data = request.data
        if not request_data:
            return APIResponse(0,'post request data not exist')
        version_number = request_data.get('ver_num')
        model_url = request_data.get('model_url')
        if not (version_number and model_url):
            return APIResponse(0,'ver_num and model_url is empty')
        data_dic = {}
        for key in request_data:
            if key == "ver_num":
                continue
            data_dic[key] = request_data.get(key)
        data_dic['version_number'] = version_number
        model_obj = models.ModelVersion.objects.create(**data_dic)
        model_data = serializers.ModelVersionSerializer(model_obj).data
        return APIResponse(1,'模型版本添加成功',results=model_data)

    # 单局部改
    # 参数："station_id":"0101","version_number":"v1.06",
    def put(self,request,*args,**kwargs):
        version_number = request.data.get('version_number')
        station_id = request.data.get('station_id')
        create_time = request.data.get('create_time')
        if not (version_number and station_id and create_time):
            return APIResponse(0,'put request data is empty')
        station_obj = models.TrainStation.objects.filter(station_id=station_id).first()
        if not station_obj:
            return APIResponse(0,'station data is exist')
        station_obj.current_model_version = version_number
        station_obj.model_version_create_time = create_time
        station_obj.save()
        station_data = serializers.TrainStationSerializer(station_obj).data
        return APIResponse(1,'模型版本应用成功',results=station_data)
    # 单删
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return APIResponse(0,'pk not exist')
        model_obj = models.ModelVersion.objects.filter(id=pk).delete()
        if not model_obj:
            return APIResponse(0,'the data in the database is exist')
        model_data = serializers.ModelVersionSerializer(model_obj).data
        return APIResponse(1,'模型版本删除成功',results=model_data)

# /images/
class StationImagesAPIView(ListAPIView,DestroyAPIView):
    """车站管理的车站图纸的所有操作"""
    queryset = models.StationImage.objects.all()
    serializer_class = serializers.StationImageSerializer

    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ['station_id']
    # 群查
    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return APIResponse(results=response.data)
    # 单增
    def post(self,request,*args,**kwargs):
        image_name = request.data.get('im_name')
        image_url = request.data.get('im_url')
        station_id = request.data.get('station_id')
        founder = request.data.get('founder')
        if not (image_name and image_url and station_id and founder):
            return APIResponse(0, 'post request data not exist')

        data_dic = {}
        image_format = str(image_url).rsplit(".", 1)[1]
        data_dic["image_name"] = image_name
        data_dic["image_url"] = image_url
        data_dic["station_id"] = station_id
        data_dic["founder"] = founder
        data_dic['image_format'] = image_format
        img_obj = models.StationImage.objects.create(**data_dic)
        image_data = serializers.StationImageSerializer(img_obj).data
        return APIResponse(1,'车站图纸保存成功',results=image_data)
    # 单局部改
    def put(self,request,*args,**kwargs):
        image_name = request.data.get('image_name')
        station_id = request.data.get('station_id')
        im_url = request.data.get('image_url')
        if not (image_name and station_id and im_url):
            return APIResponse(0, 'put request data is empty')
        station_obj = models.TrainStation.objects.filter(station_id=station_id).first()
        if not station_obj:
            return APIResponse(0, 'station data is exist')
        image_url = im_url.split('/', 4)[-1]
        station_obj.current_image_name = image_name
        station_obj.station_pic = image_url
        station_obj.save()
        station_data = serializers.TrainStationSerializer(station_obj).data
        return APIResponse(1, '车站图纸应用成功', results=station_data)

    # 单删
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return APIResponse(0, 'pk not exist')
        image_obj = models.StationImage.objects.filter(id=pk).delete()
        image_data = serializers.StationImageSerializer(image_obj).data
        return APIResponse(1, '模型版本删除成功', results=image_data)

class SchemesAPIView(ListAPIView,RetrieveAPIView,CreateAPIView):
    """仿真方案相关操作"""
    queryset = models.TrainScheme.objects.all()
    serializer_class = serializers.TrainSchemeSerializer
    filter_backends = [DjangoFilterBackend]
    # 按照车站编号对模型版本进行过滤
    filter_fields = ["station_id","is_run"]
    # 群查展示所有的仿真方案
    def get(self, request, *args, **kwargs):
        scheme_id = request.query_params.get('scheme_id')
        if not scheme_id:
            station_id = request.query_params.get('station_id')
            station_list = list(TransStation.objects.filter(station_id=station_id).values_list("station_code",flat=True))
            if not station_list:
                response = self.list(request,*args,**kwargs).data
                return APIResponse(results=response)
            train_queryset = models.TrainScheme.objects.filter(station_id__in=station_list).all()
            response = []
            for train in train_queryset:
                for train_obj in train:
                    scheme_data = serializers.TrainSchemeSerializer(train_obj,many=True).data
                    response.append(scheme_data)
            return APIResponse(results=response)
        scheme_query = models.TrainScheme.objects.filter(scheme_id=scheme_id).all()
        scheme_data = serializers.TrainSchemeSerializer(scheme_query,many=True).data
        return APIResponse(results=scheme_data)

    # 新建一个仿真方案
    def post(self,request,*args,**kwargs):
        response = self.create(request,*args,**kwargs)
        return APIResponse(results=response.data)

    # 单删一个仿真方案
    def delete(self, request, *args, **kwargs):
        pk = request.data.get("scheme_id")
        if not pk:
            return APIResponse(0, 'pk not exist')
        scheme_obj = models.TrainScheme.objects.filter(scheme_id=pk).delete()
        scheme_data = serializers.TrainSchemeSerializer(scheme_obj).data
        return APIResponse(1, '模型版本删除成功', results=scheme_data)
    # 单局部更新
    def patch(self, request, *args, **kwargs):
        request_data = request.data
        step = request_data.pop('step',None)
        scheme_id = request_data.get('scheme_id',None)
        if not (step and scheme_id and request_data):
            return APIResponse(0,'step and scheme_id not exist')
        if step not in [1,2,3,4]:
            return APIResponse(0,'step is not valid number')
        if step == 1:
            scheme_name = request_data.get('scheme_name')
            editer = request_data.get('editer')
            if not (scheme_name and editer):
                return APIResponse(0,'scheme_name is empty')
        elif step == 2:
            period_list = request.data.pop('period_list', None)
            if not period_list:
                return APIResponse(0, 'period_list is null')
            first_time, second_time = period_list
            start_time = first_time + ":00"
            end_time = second_time + ":00"
            request_data['start_time'] = start_time
            request_data['end_time'] = end_time
        elif step == 3:
            ps_pare_type = request_data.get('ps_pare_type')
            if not ps_pare_type:
                return APIResponse(0,'ps_pare_type is empty')
        else:
            is_run = request_data.get('is_run')
            if not is_run:
                return APIResponse(0,'is_run is empty')
        scheme_query = models.TrainScheme.objects.filter(scheme_id=scheme_id).first()
        print(request_data)
        scheme_obj = serializers.TrainSchemeSerializer(instance=scheme_query, data=request_data, partial=True)
        scheme_obj.is_valid(raise_exception=True)
        scheme_ob = scheme_obj.save()
        data = serializers.TrainSchemeSerializer(scheme_ob).data
        return APIResponse(1, '方案更新成功',results=data)

import json
import requests
class AuthAPIView(APIView):
    def get(self,request,*args,**kwargs):
        access_token = request.query_params.get('tk')
        if not access_token:
            return APIResponse(0,'the token is None')
        url = BASE_URL + "features"
        headers = {
            "Authorization":"Bearer"+ f"{access_token}",
            "Accept":"Application/json",
        }

        """
        http://122.51.26.86:42080/stationsimulation/?tk=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTU1OTEzOTAsInVzZXJfbmFtZSI6Ijk1MjciLCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiNmZmYmM2NzktMjdhMi00ZmZjLTk4MmItMjc1MzY5Nzg1NWM3IiwiY2xpZW50X2lkIjoiZm9vQ2xpZW50SWRQYXNzd29yZCIsInNjb3BlIjpbImZvbyIsInJlYWQiLCJ3cml0ZSJdfQ.UhvtMjUY7JjmxTCg9sk2wb0q8pVLxbY-7vwuoNjz26gD4dMn66Y_oTmtW2vIzoefTbgRhSuVWHTcIC1nXk1UfTUwM88v1YsbtIq3gFkAWsV3HTxYg01P7c4NMHK_gfDMg2Jt3ghE7mj49QZ0Rcrt6y2LN6njtK0175jfCgGJ-8M84tOGoPMA-euYD31pUZKpHvgdEE5KX97_FxL-afdE23sEpBXd8nW2XaeY5nPXwc_rQtnx25ibZGE6CK7kiebplM7hxFz8iWgN7XoxFSScaR0MT1_bCA-A5cOK-7FKBM2aFOlyyj0b6HB6YPRN4QWUrWqHDz60FObEIGZGMk21yw#/homepage
        """
        # 获取当前登录用户的功能权限
        response = json.loads(requests.get(url,headers=headers).text)
        if not response:
            return APIResponse(0, 'User does not have permission')
        if FUNC_ID not in response:
            return APIResponse(0,"User does not have permission")

        url2 = BASE_URL + "userinfo"
        # 获取当前登录用户的个人信息（包含部门信息）
        res = json.loads(requests.get(url2, headers=headers).text)
        if not res:
            return APIResponse(0,'No User Info')
        return APIResponse(results=res)































