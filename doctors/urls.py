from django.urls import path
from .views import DoctorVerification

urlpatterns = [
    path(
        "doctor_verification/",
        DoctorVerification.as_view(),
        name="doctor_verfication",
    ),
    path("edit_requests/<int:id>", DoctorVerification.as_view(), name="edit_requests"),
]
