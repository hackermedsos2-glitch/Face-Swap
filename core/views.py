from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TosVersion


def tos_view(request):
    tos = TosVersion.get_active()
    return render(request, "core/tos.html", {"tos": tos})


@login_required
def home_view(request):
    # Placeholder Tahap 1 — endpoint generate/face-swap belum aktif.
    return render(request, "core/home.html")
