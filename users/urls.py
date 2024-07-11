from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import Registration, Logout, PasswordRecovery, OTPVerfication

urlpatterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", Registration.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("forgot_password/", PasswordRecovery.as_view(), name="forgot_password"),
    path("set_password/", OTPVerfication.as_view(), name="set_password"),
]
