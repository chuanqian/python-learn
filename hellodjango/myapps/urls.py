from django.urls import path
from . import views

urlpatterns = [
    path("addInfo/",views.addPersonInfo,name="addPersonInfo"),
]