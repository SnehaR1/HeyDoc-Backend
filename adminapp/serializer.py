from rest_framework import serializers
from .models import Department, Doctors


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    dept_name = serializers.CharField(source="department.dept_name", read_only=True)

    class Meta:
        model = Doctors
        fields = [
            "department",
            "doc_id",
            "doc_name",
            "dept_name",
            "doc_image",
            "isDeptHead",
            "phone",
            "email",
            "isActive",
        ]
