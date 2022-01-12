from django.urls import path
from . import views

urlpatterns = [
    # registrations route
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # home
    path("", views.home, name="home"),
    # user
    path("user-home/", views.userHome, name="userHome"),
    # admin
    path("admin-home/", views.adminHome, name="adminHome"),
    path("admin-chat/<int:userId>/", views.adminChat, name="adminChat"),
]
