from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment
from .forms.access import LoginForm, RegisterForm
from .forms.admin import EditUserForm, ChangePasswordForm, AddUserForm
from .forms.messages import MessageForm, CommentForm
import bcrypt
from django.template.defaulttags import register


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


def registration(request):

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


def admin_add_user(request):

    if "user_id" in request.session:
        user = User.objects.filter(id=request.session["user_id"])
        if user:
            logged_user = user[0]

            if logged_user.level == 9:

                if request.method == "GET":
                    add_user_form = AddUserForm()

                if request.method == "POST":

                    add_user_form = EditUserForm(request.POST)
                    if add_user_form.is_valid():
                        password = request.POST["password"]
                        pw_hash = bcrypt.hashpw(password.encode(),
                                    bcrypt.gensalt()).decode()
                        new_user = User()
                        new_user.password_hash = pw_hash
                        new_user.email = request.POST["email"]
                        new_user.first_name = request.POST["first_name"]
                        new_user.last_name = request.POST["last_name"]
                        new_user.level = request.POST["level"]
                        new_user.save()
                        return redirect('/dashboard/admin')

                log_url, log_text = set_log_link(request.session)
                context = {"add_user_form": add_user_form,
                           "log_text": log_text,
                           "log_url": log_url}

                return render(request, "add_user.html", context)

            else:
                return redirect('/dashboard')

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


def show_messages(request, id):

    if "user_id" not in request.session:
        return redirect('/')

    user = User.objects.filter(id=id)
    if not user:
        return redirect('/')

    user_showing = user[0]
    user_posting = User.objects.get(id=request.session["user_id"])

    messages = user_showing.received_messages.order_by("-created_at")
    comment_forms = create_comment_forms(messages)

    if request.method == "GET":
        message_form = MessageForm()

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            posted_message = message_form.save(commit=False)
            posted_message.recipient_user = user_showing
            posted_message.sender_user = user_posting
            posted_message.save()
            return redirect('/users/show/' + str(id))

    log_url, log_text = set_log_link(request.session)
    context = {
        "user_showing": user_showing,
        "messages": messages,
        "message_form": message_form,
        "comment_forms": comment_forms,
        "log_text": log_text,
        "log_url": log_url
    }

    return render(request, "user_wall.html", context)


def new_comment(request, user_showing_id):

    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        message_commented_id = request.POST["message_commented_id"]
        message_commented = Message.objects.get(id=message_commented_id)
        print(message_commented.content)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.message = message_commented
            comment.user = User.objects.get(id=request.session["user_id"])
            print(user_showing_id, request.session["user_id"])
            comment.save()

    return redirect('/users/show/' + str(user_showing_id))


def create_comment_forms(messages):
    comment_forms = {}
    for message in messages:
        comment_forms[message.id] = CommentForm(
            initial={"message_commented_id": message.id}
        )
    return comment_forms


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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

