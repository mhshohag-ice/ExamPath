
from django.urls import path
from . import views
urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("<slug:slug>/", views.exam_detail, name="exam_detail"),
    path("<slug:slug>/subjects/", views.exam_subjects, name="exam_subjects"),
]
