from django.urls import path
from .views import Departments, EditDepartment, Doctor, AdminLogin, DashBoard, Users

urlpatterns = [
    path("departments/", Departments.as_view(), name="departments"),
    path("department/<str:id>/", EditDepartment.as_view(), name="department"),
    path("doctors/", Doctor.as_view(), name="doctors"),
    path("admin_login/", AdminLogin.as_view(), name="admin_login"),
    path("admin_dashboard/", DashBoard.as_view(), name="admin_dashboard"),
    path("users/", Users.as_view(), name="users"),
    path("user/<int:id>/", Users.as_view(), name="edit_users"),
]
