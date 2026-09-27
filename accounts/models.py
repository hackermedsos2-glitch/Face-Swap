from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Consent — wajib dicentang saat registrasi
    agreed_own_face_only = models.BooleanField(default=False)
    tos_version_accepted = models.ForeignKey(
        "core.TosVersion", null=True, blank=True, on_delete=models.SET_NULL
    )
    tos_accepted_at = models.DateTimeField(null=True, blank=True)

    # Rate limiting harian — dipakai mulai Tahap 2, kolomnya disiapkan sejak sekarang
    daily_generate_limit = models.PositiveIntegerField(default=10)
    generate_count_today = models.PositiveIntegerField(default=0)
    generate_count_reset_at = models.DateField(null=True, blank=True)

    # Moderasi akun
    is_banned = models.BooleanField(default=False)
    banned_at = models.DateTimeField(null=True, blank=True)
    ban_reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    @property
    def is_fully_verified(self):
        return self.email_verified_at is not None


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"OTP untuk {self.user.email} ({'terpakai' if self.is_used else 'aktif'})"

    def is_valid(self):
        return (not self.is_used) and timezone.now() < self.expires_at
