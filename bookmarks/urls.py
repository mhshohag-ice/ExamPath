
from django.urls import path
from . import views
urlpatterns = [
    path("", views.bookmark_list, name="bookmarks"),
    path("my/", views.my_questions, name="my_questions"),
]
