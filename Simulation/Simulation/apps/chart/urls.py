from django.urls import path
from . import views
urlpatterns = [
    path('fac/', views.FacAPIView.as_view()),
]