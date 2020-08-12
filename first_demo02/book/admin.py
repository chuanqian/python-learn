from django.contrib import admin
from .models import Subject, Teacher


# Register your models here.

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ("no", "name", "intro", "is_host")
    search_fields = ("name",)
    ordering = ("no",)


class TeacherMoodelAdmin(admin.ModelAdmin):
    list_display = ("no", "name", "sex", "birth", "good_count", "bad_count", "subject")
    search_fields = ("name",)
    ordering = ("no",)


admin.site.register(Subject, SubjectModelAdmin)
admin.site.register(Teacher, TeacherMoodelAdmin)
