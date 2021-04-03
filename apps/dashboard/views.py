from django.shortcuts import render
from .models import User
from .forms.access import LoginForm


def index(request):
    return render(request, "index.html")


def login(request):

    if request.method == "GET":
        login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)

    return render(request, "login.html", {"login_form": login_form})
