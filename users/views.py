from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        # Accessing username and password from data
        username = request.POST["username"]
        password = request.POST["password"]
        # Check if the username and password are correct, returning User object if so
        user = authenticate(request, username=username, password=password)
        # If user object is returned, log in and route to the index page:
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # otherwise return login page again with new context
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
    else:
        return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })