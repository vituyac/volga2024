from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    is_manager = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if (self.is_superuser != 1):
                self.password = make_password(self.password)
        super().save(*args, **kwargs)


