
from django.contrib import admin
from .models import ExamFamily, ExamSession
@admin.register(ExamFamily)
class ExamFamilyAdmin(admin.ModelAdmin):
    list_display = ("name","slug","active")
    prepopulated_fields = {"slug":("name",)}
@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ("name","route_id","exam_type","specialization","exam_date","marks","question_count","status","is_demo")
    list_filter = ("status","is_demo","exam_type","specialization")
    search_fields = ("name","route_id")
    ordering = ("-exam_date",)
