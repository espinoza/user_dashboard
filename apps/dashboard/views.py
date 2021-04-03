from django.shortcuts import render, redirect, HttpResponse
from .models import User
from .forms.access import LoginForm, RegisterForm
from .forms.admin import EditUserForm, ChangePasswordForm
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

            users = User.objects.filter(level=9)
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


def dashboard_admin(request):

    if "user_id" in request.session:
        user = User.objects.filter(id=request.session["user_id"])
        if user:
            logged_user = user[0]

            if logged_user.level == 9:
                log_url, log_text = set_log_link(request.session)
                users = User.objects.all()
                context = {"users": users,
                           "is_admin": True,
                           "log_text": log_text,
                           "log_url": log_url}
                return render(request, "dashboard.html", context)
            else:
                return redirect('/dashboard')

    return redirect('/')


def dashboard(request):

    if "user_id" in request.session:
        user = User.objects.filter(id=request.session["user_id"])
        if user:
            logged_user = user[0]

            if logged_user.level == 9:
                return redirect('/dashboard/admin')
            else:
                log_url, log_text = set_log_link(request.session)
                users = User.objects.all()
                context = {"users": users,
                           "is_admin": False,
                           "log_text": log_text,
                           "log_url": log_url}
                return render(request, "dashboard.html", context)

    return redirect('/')


def admin_edit_user(request, id):

    if "user_id" in request.session:
        user = User.objects.filter(id=request.session["user_id"])
        if user:
            logged_user = user[0]

            if logged_user.level == 9:

                user_with_id = User.objects.filter(id=id)
                if not user_with_id:
                    return redirect('/dashboard/admin')
                user_to_edit = user_with_id[0]

                if request.method == "GET":
                    edit_user_form = EditUserForm(instance=user_to_edit)

                if request.method == "POST":

                    if id == request.session["user_id"]:
                        if request.POST["level"] != 9:
                            response = not_allowed("leave admin level by yourself")
                            return response

                    edit_user_form = EditUserForm(request.POST,
                                                  instance=user_to_edit)
                    if edit_user_form.is_valid():
                        edit_user_form.save()
                        return redirect('/dashboard/admin')

                change_password_form = ChangePasswordForm()
                log_url, log_text = set_log_link(request.session)
                context = {"edit_user_form": edit_user_form,
                           "change_password_form": change_password_form,
                           "user_to_edit_id": user_to_edit.id,
                           "log_text": log_text,
                           "log_url": log_url}

                return render(request, "edit_user.html", context)

            else:
                return redirect('/users/edit')

    return redirect('/')


def admin_change_password(request, id):

    user = User.objects.filter(id=id)
    if not user:
        return redirect('/dashboard/admin/')
    user_to_edit = user[0]
    edit_user_form = EditUserForm(instance=user_to_edit)

    if request.method == "GET":
        return redirect('/dashboard/admin/')

    if request.method == "POST":
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(),
                                    bcrypt.gensalt()).decode()
            user_to_edit.password_hash = pw_hash
            user_to_edit.save()
            return redirect('/users/edit/' + str(id))
        else:
            log_url, log_text = set_log_link(request.session)
            context = {"edit_user_form": edit_user_form,
                       "change_password_form": change_password_form,
                       "user_to_edit_id": user_to_edit.id,
                       "log_text": log_text,
                       "log_url": log_url}
            return render(request, "edit_user.html", context)


def admin_remove_user(request, id):

    if "user_id" in request.session:
        user = User.objects.filter(id=request.session["user_id"])
        if user:
            logged_user = user[0]
            if logged_user.level == 9:

                if id == request.session["user_id"]:
                    response = not_allowed("remove yourself")
                    return response

                user = User.objects.filter(id=id)
                if user:
                    user_to_remove = user[0]
                    user_to_remove.delete()

    return redirect('/dashboard/admin')


def set_log_link(request_session):
    if "user_id" in request_session:
        log_text = "Log out"
        log_url = "/logout"
    else:
        log_text = "Log in"
        log_url = "/login"
    return log_url, log_text


def not_allowed(action_string):
    response = HttpResponse()
    response.write("<p>You can't " + action_string + "!</p>")
    response.write("<p>Ask another admin to do that.</p>")
    response.write("<p><a href='/dashboard/admin'>Go to dashboard</a></p>")
    return response
