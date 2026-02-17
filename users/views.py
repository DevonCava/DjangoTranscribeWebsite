from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login # called auth_login to avoid name conflict with our login view
from django.contrib.auth import logout as auth_logout

def users(request):
    allUsers = get_user_model().objects.all()
    return render(request, "users.html", {"allUsers": allUsers})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST) # authentication form needs specified data parameter
        if form.is_valid():
            auth_login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("posts:list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logoutUser(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("users:login")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth_login(request, form.save()) # saves form/user and logs them in
            return redirect("users:login") ## reference which app, and then which view
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
