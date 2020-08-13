from django.http import JsonResponse
from django.urls import path
from .views import show_subjects

urlpatterns = [
    path('api/subjects/', show_subjects),
]