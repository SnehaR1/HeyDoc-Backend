from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import DepartmentSerializer, DoctorSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Doctors
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from users.serializer import CustomUserSerializer
from django.contrib.auth.decorators import login_required


# Create your views here.
class AdminLogin(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if user is not None and user.is_staff:

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:

            return Response(
                {"error": "Invalid credentials or user is not an admin."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class DashBoard(APIView):
    pass


class Users(APIView):
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(
                {
                    "message": "User information successfully retrieved",
                    "users": serializer.data,
                }
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            is_active = request.data.get("block")
            if is_active == "false":
                is_active = False
                user.is_active = is_active
                user.save()
                return Response({"message": "Successfully Blocked the user"})
            else:
                is_active = True
                user.is_active = is_active
                user.save()
                return Response({"message": "Successfully Unblocked the user"})

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class Departments(APIView):

    def post(self, request):

        dept_name = request.data.get("dept_name")
        dept_description = request.data.get("dept_description")
        dept_image = request.data.get("dept_image")
        is_dept_present = Department.objects.filter(dept_name=dept_name).first()
        if is_dept_present:
            return Response(
                {"error": "Department with this name is already present"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not dept_name or not dept_description or not dept_image:
            return Response(
                {"error": "The fields can't be empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():

                serializer.save()
                return Response(
                    {"message": "Department added Successfully"},
                    status=status.HTTP_201_CREATED,
                )
            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            departments = Department.objects.all()

            serializer = DepartmentSerializer(departments, many=True)
            return Response(
                {
                    "message": "Successfully fetched department informations!",
                    "departments": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EditDepartment(APIView):
    def put(self, request, id):
        try:
            department = Department.objects.filter(dept_id=id).first()

            serializer = DepartmentSerializer(instance=department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Department Successfully Updated"},
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            department = Department.objects.filter(dept_id=id).first()
            serializer = DepartmentSerializer(department)

            return Response(
                {
                    "message": "Department Information Successfully Fetched!",
                    "department": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Doctor(APIView):

    def post(self, request):
        doc_name = request.data["doc_name"]
        department = request.data["department"]
        phone = request.data["phone"]
        email = request.data["email"]
        doc_image = request.data["doc_image"]

        if not doc_name or not department or not phone or not email or not doc_image:
            return Response({"error": "Please fill in the required fileds"})

        try:
            serializer = DoctorSerializer(data=request.data)

            if serializer.is_valid():

                serializer.save()
                return Response(
                    {"message": "Doctor successfully added!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            doctors = Doctors.objects.all()

            serializer = DoctorSerializer(doctors, many=True)
            return Response(
                {
                    "message": "Doctors info sent successfully",
                    "doctors": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
