from .models import DoctorAccountRequest
from rest_framework import serializers


class DoctorAccountRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAccountRequest
        fields = "__all__"
