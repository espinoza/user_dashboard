from django import forms
from ..models import User
from ..validations import validate_registration_password, \
    validate_registration_email, validate_login


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

        errors = validate_registration_password(password)
        if errors:
            raise forms.ValidationError({"password": errors})

        if password != confirm_password:
            raise forms.ValidationError({"confirm_password":
                                         "Passwords don't match"})

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        errors = validate_registration_email(email)
        if errors:
            raise forms.ValidationError(errors)
        return email

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

        errors = validate_login(password, email)
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

