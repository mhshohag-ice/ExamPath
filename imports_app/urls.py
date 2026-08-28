
from django.urls import path
from . import views
urlpatterns = [
    path("upload/", views.import_upload, name="import_upload"),
    path("preview/<int:job_id>/", views.import_preview, name="import_preview"),
    path("approve/<int:job_id>/", views.import_approve, name="import_approve"),
]
