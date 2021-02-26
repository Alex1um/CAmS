from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .forms import RegisterForm, LoginForm
from django.forms import Form


def register(request, next_path=''):
    if request.method == "POST":
        status, temp = validate_register(request)
        if status:
            user = temp
            if next_path:
                return redirect(request.build_absolute_uri(next_path))
            return redirect("/t")
        else:
            form = temp
    else:
        form = RegisterForm()
    # TODO: main_page
    return render(request,
                  'form-site.html',
                  {"form_title": "Register new User",
                   "form": form,
                   "action": "/u/register",
                   "title": "Sign up",
                   "page_type": "register"})


def validate_register(request) -> (bool, Form or User):
    form = RegisterForm(request.POST)
    if form.is_valid():
        data: dict = form.cleaned_data
        del data["register_repeat_password"]
        user = User.objects.create_user(**data)
        user.save()
        login(request, user)
        return True, user
    return False, form


def validate_login(request) -> (bool, Form or User):
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            user: User = User.objects.get_by_natural_key(
                data.get("login_username"))
            if user.check_password(data.get("login_password")):
                login(request, user)
                return True, user
            else:
                form.add_error("login_password", "Wrong password")
        except User.DoesNotExist:
            form.add_error("login_password", "Wrong password")
            form.add_error("login_username", "Wrong username")
    return False, form


def simple_login(request, next_path=""):
    if request.user.is_authenticated:
        return redirect(request.build_absolute_uri("/"))
    if request.method == "POST":
        status, temp = validate_login(request)
        if status:
            if next_path:
                return redirect(request.build_absolute_uri(next_path))
            return redirect("/t")
        else:
            form = temp
    else:
        form = LoginForm()
    return render(request, 'form-site.html',
                  {"form_title": "Log in",
                   "form": form,
                   "action": "/u/login",
                   "title": "Log in",
                   "page_type": "login"}
                  )


@login_required
def simple_logout(request, next_path="/"):
    logout(request)
    return redirect(next_path or "/")


def NotAllowedPath(*args, **kwargs):
    return HttpResponseNotAllowed(['register', 'login'])
