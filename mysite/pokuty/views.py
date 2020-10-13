from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from pokuty.forms import UserAdminCreationForm, LoginForm
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# def register(req):
#     form = UserAdminCreationForm()
#     if req.method == 'POST':
#         form = UserAdminCreationForm(req.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('register')
#     return render(req, "pokuty/dashboard.html")

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