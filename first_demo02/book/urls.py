from django.urls import path
from django.contrib import admin

from book.views import show_subject, show_teacher

urlpatterns = [
    path("admin/",admin.site.urls),
    path("",show_subject),
    path("teachers/",show_teacher)
]
