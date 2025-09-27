from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    # By default AbstractUser has is_active; we leave default False for new users via form save.

    def __str__(self):
        return self.username or self.email
