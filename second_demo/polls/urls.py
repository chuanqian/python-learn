from django.http import JsonResponse
from django.urls import path
from .views import show_subjects,BookViews

urlpatterns = [
    path('api/subjects/', show_subjects),
    path("api/books/",BookViews.as_view(),name="books")
]