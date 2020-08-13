from django.urls import path
from django.contrib import admin

from book.views import show_subject, show_teacher, export_teachers_excel, get_teacher_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", show_subject),
    path("teachers/", show_teacher),
    path("excel/", export_teachers_excel),
    path("teacher_data/", get_teacher_data),
    path("api/subjects/",show_subject),
]
