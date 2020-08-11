from django.urls import path, re_path
from . import views
urlpatterns = [
    path('line/', views.LineAPIView.as_view()),
    path('login/', views.AuthAPIView.as_view()),
    # 获取某个车站的信息
    re_path('^(?P<pk>\d+)/$', views.StationAPIView.as_view()),
    # 获取全部的模型版本 和 添加模型版本
    path('models/', views.ModelVersionsAPIView.as_view()),
    re_path('models/(?P<pk>\d+)/', views.ModelVersionsAPIView.as_view()),
    path('images/', views.StationImagesAPIView.as_view()),
    re_path('images/(?P<pk>\d+)/', views.StationImagesAPIView.as_view()),
    # 展示所有的仿真方案
    path('schemes/', views.SchemesAPIView.as_view()),
]