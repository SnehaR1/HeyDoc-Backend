from django.shortcuts import render
from .tasks import send_mail_task
from rest_framework.views import APIView
from django.conf import settings
from adminapp.models import Doctors
from users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from users.serializer import CustomUserSerializer
from .serializer import DoctorAccountRequestSerializer
from .models import DoctorAccountRequest
from django.core.mail import send_mail


class DoctorVerification(APIView):
    def post(self, request):

        try:
            email = request.data.get("email")
            message = request.data.get("message")
            account_exist = Doctors.objects.filter(email=email).first()
            if account_exist and account_exist.account_activated:
                return Response(
                    {"message": "Account already activated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request_exist = DoctorAccountRequest.objects.filter(email=email).first()
            if request_exist:
                return Response({"message": "A request with this email already exist."})

            isDoctor = Doctors.objects.filter(email=email).first()
            if isDoctor and isDoctor.account_activated:
                return Response(
                    {
                        "error": "The Doctor account with this mail is already activated!"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if isDoctor:
                serializer = DoctorAccountRequestSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()

                    new_message = f"Email : {email} \nMessage : {message}"
                    admin = list(
                        CustomUser.objects.filter(is_staff=True).values_list(
                            "email", flat=True
                        )
                    )

                    send_mail(
                        "Request for Doctor Account",
                        new_message,
                        settings.EMAIL_HOST_USER,
                        admin,
                    )

                    return Response(
                        {"message": "Email succesfully sent to notify the admin"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {
                        "error": "The email does not belong to any of our doctors.Try again."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        try:
            doctor_requests = DoctorAccountRequest.objects.all()
            serializer = DoctorAccountRequestSerializer(doctor_requests, many=True)
            return Response(
                {
                    "message": "Doctor account requests successfully retrieved",
                    "doc_requests": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, id):
        try:
            doc_request = DoctorAccountRequest.objects.filter(id=id)
            doc_email = doc_request.values("email")[0]["email"]
            if not doc_request:
                return Response(
                    {"error": "DoctorAccountRequest not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            message = request.data.get("message")
            print(request.data)
            doctor = Doctors.objects.filter(email=doc_email).first()
            set_password_url = f"http://localhost:3000/set_password/{doctor.doc_id}"
            email_message = (
                f"Dear Dr.{doctor.doc_name},\n\n"
                "Your account has been created. Please set your password by clicking the link below:\n\n"
                f"Please do not share this link : {set_password_url}\n\n"
                "Best regards,\n\n"
                "HeyDoc"
            )
            rejection_message = (
                f"Dear Dr.{doctor.doc_name},\n\n"
                "Your request for an account has been rejected by the admin. Please contact us for further details.\n\n"
                "Best regards,\n\n"
                "HeyDoc"
            )
            if message == "accept":
                send_mail(
                    "Welcome Aboard: Your Account is Now Verified",
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [doc_email],
                )
            elif message == "reject":
                send_mail(
                    "Doctor Account Request has been Rejected!",
                    rejection_message,
                    settings.EMAIL_HOST_USER,
                    [doc_email],
                )
            doc_request.delete()
            return Response(
                {"message": "Request processed and record deleted."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
