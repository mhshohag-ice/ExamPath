
from django.urls import path
from . import views
urlpatterns = [
    path("achievements/", views.achievements_view, name="achievements"),
    path("leaderboard/", views.leaderboard_view, name="leaderboard"),
    path("xp-history/", views.xp_history, name="xp_history"),
]
