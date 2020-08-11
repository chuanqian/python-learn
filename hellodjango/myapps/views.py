from django.shortcuts import render
from django.http import HttpResponse
from .models import Test
# Create your views here.
def addPersonInfo(request):
    test1 = Test(name="zhangqc",age=18)
    test1.save()
    return HttpResponse("<p>添加数据成功！</p>")
