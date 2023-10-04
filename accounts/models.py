from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from uuid import uuid4

from .services import get_path_upload_avatar, validate_size_image

# https://abhik-b.medium.com/step-by-step-guide-to-email-social-logins-in-django-5e5436e20591

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Users require an phone field')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
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
    objects = CustomUserManager()
    
    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.phone}'
    

    def save(self, *args, **kwargs):
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        if self.custom_id == '':
            self.custom_id = str(uuid4())[-12:]
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    about = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    skills = models.CharField(max_length=200, blank=True, null=True)
    overview = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} > profile"