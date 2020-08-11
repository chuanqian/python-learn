from django.urls import path
from . import views
urlpatterns = [
    path('gate/', views.GateStatusAPIView.as_view()),
    path('es/', views.EsCsStatusAPIView.as_view()),
    path('fen/', views.FenceStatusAPIView.as_view()),
    path('way/', views.GateWayStatusAPIView.as_view()),
    path('pscomp/', views.PsCompAPIView.as_view()),
    path('psequ/', views.PsEquipmentAPIView.as_view()),
    path('psfac/', views.PsFacilitiesAPIView.as_view()),
    path('inout/', views.InOutRateAPIView.as_view()),
    path('trainpart/', views.TrainPartRateAPIView.as_view()),
]