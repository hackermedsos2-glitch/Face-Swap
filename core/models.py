from django.db import models


class TosVersion(models.Model):
    """
    Setiap perubahan Terms of Service dicatat sebagai versi baru.
    User menyetujui versi tertentu (dicatat di accounts.User.tos_version_accepted),
    bukan sekadar centang sekali tanpa jejak versi.
    """
    version = models.CharField(max_length=50, unique=True)
    content = models.TextField(help_text="Isi ToS, boleh HTML sederhana.")
    is_active = models.BooleanField(
        default=True,
        help_text="Hanya satu versi yang sebaiknya aktif untuk user baru."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ToS {self.version}"

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first()
