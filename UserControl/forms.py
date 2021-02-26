from django import forms
from django.contrib.auth import validators
from django.contrib.auth.password_validation import *
from django.contrib.auth.models import User


def make_validator_callable(validator):
    return validator.validate


class LoginForm(forms.Form):
    login_username = forms.CharField(
        max_length=32, min_length=3,
        required=True,
        strip=False,
        validators=[
            validators.ASCIIUsernameValidator()],
        widget=forms.TextInput(
            {
                "placeholder": "Username",
                "aria-label": "Username",
                "class": "form-control"
            }
        ),
        label="Username"
    )
    login_password = forms.CharField(
        strip=False,
        required=True,
        label="Password",
        widget=forms.PasswordInput(
            {
                "placeholder": "Password",
                "aria-label": "Password",
                "class": "form-control"
            }
        ),
    )


class RegisterForm(forms.Form):
    register_username = forms.CharField(
        max_length=32, min_length=3,
        required=True,
        strip=False,
        validators=[
            validators.ASCIIUsernameValidator()],
        widget=forms.TextInput(
            {
                "placeholder": "Username",
                "aria-label": "Username",
                "class": "form-control"
            }
        ),
        label="Username"
    )

    register_first_name = forms.CharField(
        max_length=32, min_length=3,
        strip=False,
        validators=[
            validators.UnicodeUsernameValidator()],
        widget=forms.TextInput(
            {
                "placeholder": "Name",
                "aria-label": "Name",
                "class": "form-control"
            }
        ),
        label="Name",
        required=False,
    )
    register_last_name = forms.CharField(
        max_length=32,
        min_length=3,
        strip=False,
        validators=[
            validators.UnicodeUsernameValidator()],
        label="Last Name",
        widget=forms.TextInput(
            {
                "placeholder": "LastName",
                "aria-label": "LastName",
                "class": "form-control"
            }
        ),
        required=False,
    )
    register_email = forms.EmailField(
        required=True,
        validators=[validators.validators.validate_email],
        label="Email",
        widget=forms.EmailInput(
            {
                "placeholder": "Email",
                "aria-label": "Email",
                "class": "form-control"
            }
        ),
    )
    register_password = forms.CharField(
        strip=False,
        required=True,
        validators=map(make_validator_callable,
                       get_default_password_validators()),
        label="Password",
        widget=forms.PasswordInput(
            {
                "placeholder": "Password",
                "aria-label": "Password",
                "class": "form-control"
            }
        ),
    )
    register_repeat_password = forms.CharField(
        strip=False,
        required=True,
        label="Repeat Password",
        widget=forms.PasswordInput(
            {
                "placeholder": "Repeat Password",
                "aria-label": "Repeat Password",
                "class": "form-control"
            },
        ),
    )

    def clean(self):
        tmp = super().clean()
        try:
            pass1 = tmp.get("register_password")
            pass2 = tmp.get("register_repeat_password")
            if pass1 != pass2:
                self.add_error("register_repeat_password",
                               "Passwords does not match")
        except TypeError:
            pass
        try:
            if User.objects.get(username=tmp.get("register_username")):
                self.add_error("register_username", "User already exists")
        except User.DoesNotExist:
            pass
        return tmp
        # if not tmp.get("repeat_password") != tmp.get('password'):
