from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from pokuty.forms import UserAdminCreationForm, LoginForm
from django.views import generic
from django.urls import reverse
from django.utils import dateparse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Penalty, PenaltyRecord

def listview(request):
    records = PenaltyRecord.objects.all().filter(payed=False)

    return render(request, "pokuty/listview.html",{'records':records})

def teamsave(request):
    selectedusers = request.POST.getlist('user')
    selectedDate = request.POST.get('date')
    for user in selectedusers:
        userid = int(user)
        selecteduser = CustomUser.objects.get(id=userid)
        username = selecteduser.first_name +' '+ selecteduser.last_name
        penaltyId = int(request.POST.get('penalty'))
        penaltyItem = Penalty.objects.get(id=penaltyId)
        new_record = PenaltyRecord(penaltyDate= selectedDate,userId=user, user=username, penaltyName=penaltyItem.name, 
            penaltyPrice=penaltyItem.price, payed=False)
        new_record.save()
    
    return render(request, "pokuty/dashboard.html" )

def indsave(request):
    selectedpenalty = request.POST.getlist('penalty')
    selectedDate = request.POST.get('date')
    userid = request.POST.get('user')
    selecteduser = CustomUser.objects.get(id=userid)
    username = selecteduser.first_name +' '+ selecteduser.last_name
    for penalty in selectedpenalty:
        penaltyId = penalty
        penaltyItem = Penalty.objects.get(id=penaltyId)
        new_record = PenaltyRecord(penaltyDate= selectedDate,userId=selecteduser.id, user=username, penaltyName=penaltyItem.name, 
            penaltyPrice=penaltyItem.price, payed=False)
        new_record.save()
    return render(request, "pokuty/dashboard.html" )

def indTraining(request):
    users=CustomUser.objects.all()
    pokuty = Penalty.objects.all().filter(trainingPenalty=True).filter(teamPenalty=False)
    return render(request,"pokuty/individual.html",{'users': users, 'pokuty':pokuty})

def teamTraining(request):
    users=CustomUser.objects.all()
    pokuty = Penalty.objects.all().filter(trainingPenalty=True).filter(teamPenalty=True)
    return render(request,"pokuty/team.html",{'users': users, 'pokuty':pokuty})

def indMatch(request):
    users=CustomUser.objects.all()
    pokuty = Penalty.objects.all().filter(trainingPenalty=False).filter(teamPenalty=False)
    return render(request,"pokuty/individual.html",{'users': users, 'pokuty':pokuty})

def teamMatch(request):
    users=CustomUser.objects.all()
    pokuty = Penalty.objects.all().filter(trainingPenalty=False).filter(teamPenalty=True)
    return render(request,"pokuty/team.html",{'users': users, 'pokuty':pokuty})

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            {"form": UserAdminCreationForm}
        )
    elif request.method == "POST":
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))

@login_required(login_url='login')
def dashboard(request):
    
    return render(request, "pokuty/dashboard.html" )
    
class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "registration/login2.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("dashboard"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("dashboard"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})
		
def logout_user(request):
     if request.user.is_authenticated:
        logout(request)
     else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
     return redirect(reverse("login"))