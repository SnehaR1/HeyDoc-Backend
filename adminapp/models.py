from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractUser
from datetime import timedelta

# Create your models here.


class Department(models.Model):
    dept_id = ShortUUIDField(
        unique=True,
        length=5,
        max_length=10,
        prefix="dept",
        alphabet="abcdefgh12345",
    )
    dept_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    dept_description = models.CharField(null=False, blank=False)
    dept_image = models.ImageField(upload_to="dept_images/", null=True, blank=True)


class TimeSlot(models.Model):
    startTime = models.TimeField(unique=True, blank=False)
    endTime = models.TimeField(unique=True, blank=False)

    def generate_slot(self):
        time = self.startTime
        slots = []
        while time != self.endTime:

            slots.append(time + timedelta(minutes=15))
        return self.slots

    class Meta:
        abstract = True


class MorningSlot(TimeSlot):
    pass


class AfterNoonSlot(TimeSlot):
    pass


class Days(models.Model):
    day = models.DateField()
    morningSlot = models.ForeignKey(MorningSlot, on_delete=models.SET_NULL, null=True)
    afternoonSlot = models.ForeignKey(
        AfterNoonSlot, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.day


class Doctors(models.Model):
    doc_id = ShortUUIDField(
        unique=True,
        length=5,
        max_length=10,
        prefix="doc",
        alphabet="defghijk56789",
    )
    doc_name = models.CharField(max_length=50, null=False, blank=False)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, to_field="dept_id"
    )
    doc_image = models.ImageField(upload_to="doc_images/", null=True, blank=True)
    isDeptHead = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, null=False, blank=False, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(null=True, default="")
    isActive = models.BooleanField(default=True)
    account_activated = models.BooleanField(default=False)


class Availability(models.Model):
    isAvailable = models.BooleanField(default=True)
    day = models.ForeignKey(Days, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.SET_NULL, null=True)
