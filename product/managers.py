from django.db import models

class CommentManager(models.Manager):
    """“Izoh” modeli uchun model menejeri."""

    def all(self):
        """Ota-onasiz misol natijalarini qaytarish."""
        qs = super().filter(parent=None)
        return qs