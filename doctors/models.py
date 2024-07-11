from django.db import models


# Create your models here.
class DoctorAccountRequest(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True)
    message = models.CharField()
