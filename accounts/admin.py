
from django.contrib import admin
from .models import Profile, DailyActivity
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","xp_total","level","current_streak","longest_streak","last_activity_date")
    search_fields = ("user__username",)
@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ("user","date","questions_answered","xp_earned")
