from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from core.models import SoftDeleteManager, SoftDeleteModel
from django.db import models
from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager, SoftDeleteManager):
    def create_user(self, email, phone, password, **kwargs):
        if not phone:
            raise ValueError("Phone is required")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, phone, password, **kwargs)


class CustomUser(SoftDeleteModel, AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=16, db_index=True)
    image = models.ImageField(upload_to="users/avatars/", null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name()}"
