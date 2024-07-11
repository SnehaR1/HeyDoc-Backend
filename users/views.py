from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CustomUserSerializer
from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client

# Create your views here.


class Registration(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        confirm_password = request.data.get("confirm_password")
        username = request.data.get("username")
        email = request.data.get("email")
        phone = request.data.get("phone")
        email_exist = CustomUser.objects.filter(email=email)
        phone_exist = CustomUser.objects.filter(phone=phone)
        password = request.data.get("password")

        if not email or not phone or not username:
            return Response(
                {"error": "The fields can't be empty! Try again!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if email and email_exist:
            return Response(
                {"error": "Email belongs to an existing account!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if phone and phone_exist:
            return Response(
                {"error": "Phone number belongs to an existing account!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if confirm_password != password:
            return Response(
                {"error": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if serializer.is_valid():
                hashed_password = make_password(password)
                serializer.validated_data["password"] = hashed_password
                serializer.save()
                return Response(
                    {"message": "User Registered Successfully!"},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully Logged Out!!!"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PasswordRecovery(APIView):
    def post(self, request):
        email = request.data.get("email")
        if email and email.strip() == "":
            return Response({"error": "Enter a valid email!"})

        phone = request.data.get("phone")
        if phone and phone.strip() == "":
            return Response({"error": "Enter a valid phone number!"})

        email_exist = CustomUser.objects.filter(email=email).first()
        phone_exist = CustomUser.objects.filter(phone=phone).first()

        if email_exist:
            otp = self.generate_otp()

            request.session["otp"] = otp
            request.session["email"] = email
            request.session.modified = True
            request.session.save()

            self.email_otp(otp, email)
            return Response(
                {"message": "OTP successfully sent to you email!"},
                status=status.HTTP_200_OK,
            )

        elif phone_exist:
            otp = self.generate_otp()

            request.session["otp"] = otp
            request.session["phone"] = phone
            request.session.modified = True
            request.session.save()
            print("Session OTP:", request.session["otp"])

            print("Session Phone:", request.session["phone"])

            self.send_sms(otp, phone)
            return Response(
                {"message": "OTP successfully sent to you Mobile Number!"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "An account with the given credential does not exist!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def generate_otp(self):
        totp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(totp_secret, interval=30)
        otp = totp.now()
        return otp

    def email_otp(self, otp, email):
        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
        )

    def send_sms(self, otp, phone):
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_AUTH_MOBILE
        phone = "+91" + phone
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP is: {otp}", from_=twilio_phone_number, to=phone
        )


class OTPVerfication(APIView):
    def post(self, request):
        otp = request.data.get("otp")
        print(otp)
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        session_otp = request.session.get("otp")
        email = request.session.get("email")
        phone = request.session.get("phone")
        print(request.session.get("otp"))
        print(session_otp)
        if session_otp == otp:
            if not password or not confirm_password:
                return Response({"error": "Password fields cannot be Empty"})

            if password != confirm_password:
                return Response({"error": "The passwords does not match"})
            else:
                try:
                    if email:
                        user = CustomUser.objects.filter(email=email).first()
                        user.set_password(password)
                        return Response(
                            {"message": "Password Reset Successfull"},
                            status=status.HTTP_200_OK,
                        )
                    if phone:
                        user = CustomUser.objects.filter(phone=phone).first()
                        user.set_password(password)
                        return Response(
                            {"message": "Password Reset Successfull"},
                            status=status.HTTP_200_OK,
                        )

                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )
