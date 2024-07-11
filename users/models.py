from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", "password"]

    class Meta:

        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username
