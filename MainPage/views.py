from django.shortcuts import render, redirect
from django.http import HttpRequest
from UserControl.forms import RegisterForm, LoginForm
from UserControl.views import validate_login, validate_register


# Create your views here.
def StartPage(request, action=""):
    if request.user.is_authenticated:
        return redirect(f"./1")
    log_form = LoginForm()
    reg_form = RegisterForm()
    reg_check = ""
    log_check = ""
    if request.method == "POST":
        if action == "register":
            status, temp = validate_register(request)
            if not status:
                reg_form = temp
                reg_check = "checked"
        elif action == "login":
            status, temp = validate_login(request)
            if not status:
                log_check = "checked"
                log_form = temp
    return render(
        request,
        "start.html",
        {
            "register_form": reg_form,
            "register_title": "Register",
            "register_action": "action=register",
            "register_checked": reg_check,
            "login_form": log_form,
            "login_title": "Log in",
            "login_action": "action=login",
            "login_checked": log_check,
        }
    )