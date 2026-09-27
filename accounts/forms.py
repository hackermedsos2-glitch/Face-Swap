from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import TosVersion
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    agreed_own_face_only = forms.BooleanField(
        required=True,
        label="Saya hanya akan mengunggah wajah saya sendiri sebagai foto sumber.",
        error_messages={"required": "Kamu wajib menyetujui pernyataan ini untuk mendaftar."},
    )
    agreed_tos = forms.BooleanField(
        required=True,
        label="Saya sudah membaca dan menyetujui Syarat & Ketentuan.",
        error_messages={"required": "Kamu wajib menyetujui Syarat & Ketentuan untuk mendaftar."},
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        from django.utils import timezone

        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.agreed_own_face_only = self.cleaned_data["agreed_own_face_only"]

        active_tos = TosVersion.get_active()
        user.tos_version_accepted = active_tos
        user.tos_accepted_at = timezone.now()

        # Akun belum aktif penuh sampai email diverifikasi via OTP
        user.is_active = True  # tetap bisa login untuk proses verifikasi,
        # tapi akses fitur generate nanti (Tahap 2) wajib cek email_verified_at

        if commit:
            user.save()
        return user


class VerifyOTPForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        label="Kode OTP",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "one-time-code"}),
    )
