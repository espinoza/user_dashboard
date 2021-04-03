from django import forms
from ..models import User


class RegisterForm(forms.ModelForm):

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
        fields = ["email", "first_name", "last_name"]
        widgets = {"email": forms.EmailInput()}

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({"confirm_password": "Passwords don't match"})
        # TODO: create and import validate_registration_password()
        errors = validate_registration_password(password)
        if errors:
            raise forms.ValidationError({"password": errors})
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # TODO: create and import validate_registration_email()
        errors = validate_registration_email(email)
        if errors:
            raise forms.ValidationError(errors)
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        # TODO: create and import validate_first_name()
        errors = validate_first_name(first_name)
        if errors:
            raise forms.ValidationError(errors)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        # TODO: create and import validate_last_name()
        errors = validate_last_name(last_name)
        if errors:
            raise forms.ValidationError(errors)
        return last_name


class LoginForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    class Meta:

        model = User
        fields = ["email"]

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")

        # TODO: create and import validate_login()
        errors = validate_login(password, email)
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

