from .models import User
from .utils import contains_digit, contains_uppercase, is_valid_email
import bcrypt


def validate_registration_password(password):

    errors = []

    if not contains_digit(password):
        errors.append("Password needs at least one digit")

    if not contains_uppercase(password):
        errors.append("Password needs at least one uppercase letter")

    if len(password) < 8:
        errors.append("Password needs at least 8 characters")

    return errors


def validate_registration_email(email):

    errors = []

    if not is_valid_email(email):
        errors.append("Invalid email")

    user_with_email = User.objects.filter(email=email)
    if user_with_email:
        errors.append("Email is used by another user")

    return errors

def validate_login(password, email):

    errors = validate_email(email)

    user = User.objects.filter(email=email)
    if user:
        logged_user = user[0]
        if not bcrypt.checkpw(password.encode(), logged_user.password_hash.encode()):
            errors.append("Wrong password")
    else:
        errors.append("There is no user with this email")

    return errors


def validate_email(email):

    errors = []

    if not is_valid_email(email):
        errors.append("Invalid email")

    return errors


def validate_level(level):

    errors = []

    if level not in [0, 9]:
        errors.append("Level error: trying to send wrong value")

    return errors

