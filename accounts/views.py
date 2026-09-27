from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm, VerifyOTPForm
from .models import User
from .utils import generate_and_send_otp, verify_otp


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            generate_and_send_otp(user)
            request.session["pending_verification_user_id"] = user.id
            messages.info(request, "Kode verifikasi sudah dikirim ke email kamu.")
            return redirect("accounts:verify_otp")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_otp_view(request):
    user_id = request.session.get("pending_verification_user_id")
    if not user_id:
        messages.error(request, "Sesi verifikasi tidak ditemukan. Silakan daftar ulang.")
        return redirect("accounts:register")

    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect("accounts:register")

    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if verify_otp(user, code):
                del request.session["pending_verification_user_id"]
                login(request, user)
                messages.success(request, "Email berhasil diverifikasi. Selamat datang!")
                return redirect("core:home")
            form.add_error("code", "Kode OTP salah atau sudah kedaluwarsa.")
    else:
        form = VerifyOTPForm()

    return render(request, "accounts/verify_otp.html", {"form": form, "email": user.email})


def resend_otp_view(request):
    user_id = request.session.get("pending_verification_user_id")
    user = User.objects.filter(id=user_id).first() if user_id else None
    if user:
        generate_and_send_otp(user)
        messages.info(request, "Kode OTP baru sudah dikirim.")
    return redirect("accounts:verify_otp")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
