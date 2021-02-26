from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Dependence
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from django.forms import Form


def view_project(request, id: int):
    try:
        owner = False
        current: Project = Project.objects.get(id=id)
        user = request.user
        if current.allowed_users.count() > 0:
            if user.is_authenticated:
                if current.owners.get(id=user.id):
                    owner = True
                elif current.allowed_users.get(id=user.id):
                    owner = False
                else:
                    return HttpResponseForbidden("Project is private for you")
            else:
                return HttpResponseForbidden("Project is private")
        elif user.is_authenticated and current.owners.get(id=user.id):
            owner = True
        return render(
            request,
            "projects/project.html",
            {
                "project": current,
                "page_type": "project",
                "dependent": map(lambda d: (d.project_dependency, d.files.version), current.dependencies.all()),
                "dependencies": map(lambda d: (d.project, d.files.version), current.as_dependence.all()),
                "dir": current.files.last().files,
                "path": f"/p/{current.id}/{current.version}",
                "owner": owner,
                "owner_projects": user.owner_of_projects.all(),
            }
        )
    except ObjectDoesNotExist as f:
        # TODO: do something
        return HttpResponseNotFound("<h1>Project not found</h1>")


@login_required
def edit_project(request, id: int):
    current: Project = Project.objects.get(id=id)
    if request.method == "POST":
        new = dict(request.POST.items())
        current.name = new["name"]
        current.home_markdown = new["home_markdown"].strip()
        current.description = new["description"]
        current.short_description = new["short_description"]
        current.save()
        return redirect(f"/p/{current.id}")
    else:
        if current.owners.get(id=request.user.id):
            return render(
                    request,
                    "projects/project.html",
                    {
                        "project": current,
                        "page_type": "project",
                        "dependencies": map(lambda d: (d.project_dependency, d.files.version), current.dependencies.all()),
                        "dependent": map(lambda d: (d.project, d.files.version), current.as_dependence.all()),
                        "dir": current.files.last().files,
                        "path": f"/p/{current.id}/{current.version}",
                        "mode": "edit",
                        "owner": True
                    }
                )
        else:
            return HttpResponseForbidden("Edit not allowed")
    return HttpResponseNotAllowed(["GET", "POST"])


def hub(request):
    return HttpResponseNotFound("none")