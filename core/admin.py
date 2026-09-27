from django.contrib import admin
from .models import TosVersion


@admin.register(TosVersion)
class TosVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("version",)
