
from django.urls import path
from . import views
urlpatterns = [
    path("", views.question_list, name="question_list"),
    path("written/", views.written_list, name="written_list"),
    path("<int:pk>/", views.question_detail, name="question_detail"),
    path("<int:pk>/bookmark/", views.bookmark_toggle, name="bookmark_toggle"),
]
