from django.shortcuts import render, redirect
from .models import User
from .forms.access import LoginForm, RegisterForm
import bcrypt


def index(request):

    log_url, log_text = set_log_link(request.session)

    return render(request, "index.html", {"log_text": log_text,
                                          "log_url": log_url})


def login(request):

    if request.method == "GET":
        if "user_id" in request.session:
            return redirect('/')
        login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            logged_user = User.objects.get(email=request.POST["email"])
            request.session["user_id"] = logged_user.id
            return redirect('/')

    log_url, log_text = set_log_link(request.session)

    return render(request, "login.html", {"login_form": login_form,
                                          "log_text": log_text,
                                          "log_url": log_url}
                  )


def logout(request):

    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('/')


def register(request):

    if request.method == "GET":
        if "user_id" in request.session:
            return redirect('/')
        register_form = RegisterForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            registered_user = register_form.save(commit=False)

            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(),
                                    bcrypt.gensalt()).decode()
            registered_user.password_hash = pw_hash

            users = User.objects.all()
            if users:
                registered_user.level = 0
            else:
                registered_user.level = 9

            registered_user.save()
            request.session["user_id"] = registered_user.id
            return redirect('/')

    log_url, log_text = set_log_link(request.session)

    return render(request, "register.html", {"register_form": register_form,
                                             "log_text": log_text,
                                             "log_url": log_url})


def set_log_link(request_session):
    if "user_id" in request_session:
        log_text = "Log out"
        log_url = "/logout"
    else:
        log_text = "Log in"
        log_url = "/login"
    return log_url, log_text
