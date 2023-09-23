from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from uuid import uuid4

from .services import get_path_upload_avatar, validate_size_image


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=14, unique=True)
    image = models.ImageField(
        upload_to=get_path_upload_avatar, blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), validate_size_image])
    custom_id = models.CharField(
        max_length=14, blank=True)
    role = models.CharField(max_length=50)
    # following = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email}'
    

    def save(self, *args, **kwargs):
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        if self.custom_id == '':
            self.custom_id = str(uuid4())[-12:]
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
    about = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(blank=True)
    skills = models.CharField(max_length=200)
    overview = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} > profile"