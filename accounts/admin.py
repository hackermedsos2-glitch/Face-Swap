from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_banned", "email_verified_at", "date_joined")
    list_filter = ("is_banned", "is_staff", "is_superuser")
    search_fields = ("username", "email", "phone_number")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Verifikasi & Consent", {
            "fields": (
                "phone_number", "phone_verified_at", "email_verified_at",
                "agreed_own_face_only", "tos_version_accepted", "tos_accepted_at",
            )
        }),
        ("Rate Limit", {
            "fields": ("daily_generate_limit", "generate_count_today", "generate_count_reset_at")
        }),
        ("Moderasi", {
            "fields": ("is_banned", "banned_at", "ban_reason")
        }),
    )


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "expires_at", "is_used")
    list_filter = ("is_used",)
    search_fields = ("user__username", "user__email")
