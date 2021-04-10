from django import forms
from ..models import User
from ..validations import validate_email, \
    validate_registration_password, validate_level


class EditUserForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ["email", "first_name", "last_name", "level"]
        widgets = {
            "email": forms.EmailInput(),
            "level": forms.Select(choices=((0, "Normal"), (9, "Admin")))
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        errors = validate_email(email)
        if errors:
            raise forms.ValidationError(errors)
        return email

    def clean_level(self):
        level = self.cleaned_data.get("level")
        errors = validate_level(level)
        if errors:
            raise forms.ValidationError(errors)
        return level


class ChangePasswordForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    class Meta:

        model = User
        fields = []

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({
                "confirm_password": "Passwords don't match"
            })
        errors = validate_registration_password(password)
        if errors:
            raise forms.ValidationError({"password": errors})
        return cleaned_data


class AddUserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )
    class Meta:

        model = User
        fields = ["email", "first_name", "last_name", "level"]
        widgets = {
            "email": forms.EmailInput(),
            "level": forms.Select(choices=((0, "Normal"), (9, "Admin")))
        }

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({
                "confirm_password": "Passwords don't match"
            })
        errors = validate_registration_password(password)
        if errors:
            raise forms.ValidationError({"password": errors})
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        errors = validate_email(email)
        if errors:
            raise forms.ValidationError(errors)
        return email

    def clean_level(self):
        level = self.cleaned_data.get("level")
        errors = validate_level(level)
        if errors:
            raise forms.ValidationError(errors)
        return level
