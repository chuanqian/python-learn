from io import BytesIO

import xlwt
from django.contrib.admin.utils import quote
from django.db.models import Avg

from django.shortcuts import render, redirect

from .models import Subject, Teacher
from django.http import HttpRequest, HttpResponse, JsonResponse
from .SubejctMapper import SubjectMapper


# Create your views here.

def show_subject(request):
    # 第一种
    # queryset = Subject.objects.all()
    # subjects = []
    # for subject in queryset:
    #     subjects.append({
    #         "no": subject.no,
    #         "name": subject.name,
    #         "intro": subject.intro,
    #         "isHost": subject.is_host
    #     })
    # return JsonResponse(subjects, safe=False)
    # 第二种
    queryset = Subject.objects.all()
    subjects = []
    for subject in queryset:
        subjects.append(SubjectMapper(subject).as_dict())
    return JsonResponse(subjects, safe=False)
    # subjects = Subject.objects.all().order_by("no")
    # return render(request, "subjects.html", {"subjects": subjects})


def show_teacher(request):
    try:
        sno = int(request.GET.get("sno"))
        teachers = []
        if sno:
            subject = Subject.objects.only("name").get(no=sno)
            teachers = Teacher.objects.filter(subject=subject).order_by("no")
        return render(request, "teachers.html", {
            "subject": subject,
            "teachers": teachers
        })
    except (ValueError, Subject.DoesNotExist):
        return redirect("/")


def login(request: HttpRequest) -> HttpResponse:
    hint = ""
    return render(request, "login.html", {"hint": hint})


def export_teachers_excel(request):
    # 创建工作簿
    wb = xlwt.Workbook()
    # 添加工作表
    sheet = wb.add_sheet("老师信息表")
    # 查询所有老师的信息
    # queryset = Teacher.objects.all()
    # queryset = Teacher.objects.all().select_related("subject")
    # queryset = Teacher.objects.all().only("name","good_count","bad_count")
    # queryset = Teacher.objects.values("subject").annotate(good=Avg('good_count'), bad=Avg('bad_count'))
    queryset = Teacher.objects.values("subject").annotate(good=Avg('good_count'), bad=Avg('bad_count'))
    # 向Excel表单中写入表头
    colnames = ("姓名", "介绍", "好评数", "差评数", "学科")
    for index, name in enumerate(colnames):
        sheet.write(0, index, name)
    props = ("name", "detail", "good_count", "bad_count", "subject")
    # 向单元格中写入老师的数据
    for row, teacher in enumerate(queryset):
        for col, prop in enumerate(props):
            value = getattr(teacher, prop, "")
            if isinstance(value, Subject):
                value = value.name
            sheet.write(row + 1, col, value)
    # 保存Excel
    buffer = BytesIO()
    wb.save(buffer)
    # 将二进制数据写入相应的消息体中并设置MIME类型
    resp = HttpResponse(buffer.getvalue(), content_type="application/vnd.ms-excel")
    # 中文文件名需要处理成百分号编码
    filename = quote("老师.xls")
    # 通过响应头告知浏览器下载该文件以及对应的文件名
    resp["content-disposition"] = f'attachment; filename*=utf-8''{filename}'
    return resp


def get_teacher_data(request):
    queryset = Teacher.objects.all()
    names = [teacher.name for teacher in queryset]
    good_counts = [teacher.good_count for teacher in queryset]
    bad_counts = [teacher.bad_count for teacher in queryset]
    return JsonResponse({"names": names, "good": good_counts, "bad": bad_counts})
