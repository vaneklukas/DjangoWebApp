from django.conf.urls import url, include 
from pokuty.views import dashboard, register, UzivatelViewLogin 
from pokuty.views import indTraining, teamTraining, indMatch, teamMatch
from pokuty.views import indsave, teamsave, listview
from django.urls import path

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^registration/login2", register, name="login"),
    path("login/", UzivatelViewLogin.as_view(), name = "login"),
    url(r"^indTraining/", indTraining, name="indTraining"),
    url(r"^teamTraining/", teamTraining, name="teamTraining"),
    url(r"^indMatch/", indMatch, name="indMatch"),
    url(r"^teamMatch/", teamMatch, name="teamMatch"),
    url(r"^indsave/", indsave, name="indsave"),
    url(r"^teamsave/", teamsave, name="teamsave"),
    url(r"^listview/", listview, name="listview"),

]