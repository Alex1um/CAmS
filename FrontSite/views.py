from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def FrontPage(request, id: int):
    try:
        current = Projects.objects.get(id=id)
    except ObjectDoesNotExist as f:
        # TODO: do something
        return HttpResponseNotFound("<h1>Project not found</h1>")
    url = f"{request.scheme}://{request.get_host()}/"
    params = {
        "dependencies": list(
            {
                "link": url + str(e.Parent.id),
                "name": e.Parent.Name,
                "alert": e.Status,
                "status": str(e.get_Status_display())
            }
            for e in Dependence.objects.filter(Dependence_id=id)),
        "codependents": tuple(
            {
                "link": url + str(e.Dependence.id),
                "name": e.Dependence.Name,
                "version": "1.0.0"
            }
            for e in Dependence.objects.filter(Parent_id=id)),
        "UserProjects": tuple(
            {
                "link": url + str(e.id),
                "name": e.Name,
            }
        for e in User.objects.get(id=request.user.id).owners.all()) if request.user.is_authenticated else None,
        "Home": current.Home_html,
        "ProjectName": current.Name,
    }
    return render(request, "front.html", params)


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


def StartPage(request):
    if request.user.is_authenticated:
        return redirect(f"./1")
    if request.method == "POST":
        keys = {k[9:]:v for k, v in request.POST.items() if "register-" in k}
        if keys:
            if keys['repeat-password'] == keys["password"]:
                del keys['repeat-password']
            user = User.objects.create_user(**keys)
            user.save()
            login(request, user)
            return redirect(f"/1")
        else:
            username = request.POST["login-username"]
            password = request.POST["login-password"]
            try:
                temp = User.objects.get(email=username)
                username = temp
            except Exception:
                pass
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(f"/1")
    return render(request, "start.html")


from django.contrib.auth import logout


def Logout(request):
    red = "/"
    if pth := request.get_full_path():
        if ind := pth.find("?next="):
            red = pth[ind + 6:]
    logout(request)
    return redirect(red)