from django.contrib import admin
from .models import UserProfile, UserSessionToken,ActivityLog

admin.site.register(UserProfile)
admin.site.register(UserSessionToken)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display=("user","action","created_at")
    list_filter=("user","created_at")
    search_fields=("user__username","action")
    ordering=("-created_at",)
