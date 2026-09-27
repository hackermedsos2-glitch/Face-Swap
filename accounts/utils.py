import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import EmailOTP


def generate_and_send_otp(user) -> EmailOTP:
    """Buat kode OTP baru untuk user dan kirim lewat email."""
    code = f"{random.randint(0, 999999):06d}"
    expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

    otp = EmailOTP.objects.create(user=user, code=code, expires_at=expires_at)

    send_mail(
        subject="Kode verifikasi akun kamu",
        message=(
            f"Halo {user.username},\n\n"
            f"Kode verifikasi kamu: {code}\n"
            f"Kode ini berlaku {settings.OTP_EXPIRY_MINUTES} menit.\n\n"
            f"Kalau kamu tidak merasa mendaftar, abaikan email ini."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return otp


def verify_otp(user, code: str) -> bool:
    """Cek kode OTP terbaru milik user. Return True kalau valid & cocok."""
    otp = user.otps.filter(is_used=False).order_by("-created_at").first()
    if not otp or not otp.is_valid():
        return False
    if otp.code != code:
        return False

    otp.is_used = True
    otp.save(update_fields=["is_used"])

    user.email_verified_at = timezone.now()
    user.save(update_fields=["email_verified_at"])
    return True
