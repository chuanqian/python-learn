from django.urls import path
from . import views
urlpatterns = [
    # 正常方案客流数据请求与预测方案客流数据预设
    path('psreqes/', views.PsRequest.as_view()),
    # 正常方案行车数据请求与预测方案行车数据预设
    path('drreqes/', views.DrRequest.as_view()),
    # 预测方案客流数据导入
    path('psimport/', views.PsImport.as_view()),
    # 预测方案行车数据导入
    path('drimport/', views.DrImport.as_view()),
    # 查看客流数据
    path('passflows/', views.PassFlow.as_view()),
    # 查看行车数据
    path('drivings/', views.Driving.as_view()),

    path('emugate/', views.EmuGateStatusAPIView.as_view()),
    path('emues/', views.EmuEsCsStatusAPIView.as_view()),
    path('emufen/', views.EmuFenceStatusAPIView.as_view()),
    path('emuway/', views.EmuGateWayStatusAPIView.as_view()),
    path('emupscomp/', views.EmuPsCompAPIView.as_view()),
    path('emupsequ/', views.EmuPsEquipmentAPIView.as_view()),
    path('emupsfac/', views.EmuPsFacilitiesAPIView.as_view()),
    path('emuinout/', views.EmuInOutRateAPIView.as_view()),
    path('emutrainpart/', views.EmuTrainPartRateAPIView.as_view()),
    # 给模型提供数据
    path('simation/', views.SimationAPIView.as_view()),
    # 获取模型输出的sql语句
    path('simout/', views.SimulationOutputAPIView.as_view()),
# 给模型提供数据
    # path('sim/', views.SimAPIView.as_view()),
]
