from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Subject
from .SubjectMapper import SubjectMapper
from django.http import HttpResponse, HttpRequest
from .SubjectSerializer import SubjectSerializer
from django.views import View
from .models import BookInfo
from .EntitySerializer import BookInfoSerializer


# Create your views here.
# 原来的风格
# def show_subjects(request):
#     queryset = Subject.objects.all()
#     subjects = []
#     for subject in queryset:
#         subjects.append(SubjectMapper(subject).as_dict())
#     return JsonResponse(subjects, safe=False)

# rest_framework
@api_view(("GET",))
def show_subjects(request: HttpRequest) -> HttpResponse:
    subjects = Subject.objects.all().order_by("no")
    # 创建序列化器对象并指定要序列化的模型
    serializer = SubjectSerializer(subjects, many=True)
    # 通过序列化器的data的属性获得模型对应的字典并通过创建Response对象返回json格式的数据
    return Response(serializer.data)


class BookViews(View):

    def post(self, request):
        """查询所有图书"""
        books = BookInfo.objects.all().order_by("-id")
        ser = BookInfoSerializer(books, many=True)
        data = ser.data
        return JsonResponse(data, safe=False)
