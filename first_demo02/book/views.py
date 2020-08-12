from django.shortcuts import render, redirect
from .models import Subject, Teacher
from django.http import HttpRequest, HttpResponse


# Create your views here.

def show_subject(request):
    subjects = Subject.objects.all().order_by("no")
    return render(request, "subjects.html", {"subjects": subjects})


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
