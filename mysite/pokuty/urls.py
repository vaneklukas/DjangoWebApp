from django.conf.urls import url, include 
from pokuty.views import dashboard, register, UzivatelViewLogin
from django.urls import path

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^registration/login2", register, name="login"),
    path("login/", UzivatelViewLogin.as_view(), name = "login"),
]