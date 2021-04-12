from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project, Dependence, Version
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from django.forms import Form


def view_project(request, id: int):
    try:
        owner = False
        available_to_add = None
        current: Project = Project.objects.get(id=id)
        temp = request.GET.get("version")
        version: Version = Version.objects.get(
            uuid=temp) if temp else current.versions.first()
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
        if user.is_authenticated:
            available_to_add = user.owner_of_projects.all()
        return render(
            request,
            "projects/project.html",
            {
                "project": current,
                "page_type": "project",
                "dependent": map(lambda d: (d.project, d.project.versions.first().name), current.as_dependence.all()),
                "dependencies": map(lambda d: (d.project_dependency, d.project_dependency_version.name), current.dependencies.all()),
                "dir": version.files,
                "path": f"/p/{current.id}",
                "owner": owner,
                "owner_projects": available_to_add,
                "version": version,
                "title": current.name,
            }
        )
    except ObjectDoesNotExist as f:
        # TODO: do something
        return HttpResponseNotFound("<h1>Project not found</h1>")


import uuid


@login_required
def edit_project(request, id: int):
    current: Project = Project.objects.get(id=id)
    temp = request.GET.get("version")
    version: Version = Version.objects.get(uuid=temp) if temp else current.versions.first()
    if request.method == "POST":
        version_type = request.POST['version-chooser-type']
        if version_type == "old":
            new_version = current.versions.get(uuid=request.POST["version-uuid-select"])
        else:
            new_version = Version()
            new_version.project = current
            new_version.files = version.files
            new_version.uuid = request.POST['version-uuid']
        new_version.name = request.POST["version-name"]
        new_version.description = request.POST["description"]
        new_version.short_description = request.POST["short_description"]
        new_version.home_markdown = request.POST["home_markdown"]
        new_version.save()
        current.name = request.POST["name"]
        current.save()
        return redirect(f"p/{current.id}")
    else:
        if current.owners.get(id=request.user.id):
            return render(
                    request,
                    "projects/project-edit.html",
                    {
                        "project": current,
                        "page_type": "project",
                        "dependencies": map(lambda d: (d.project_dependency, "0"), current.dependencies.all()),
                        "dependent": map(lambda d: (d.project, "0"), current.as_dependence.all()),
                        "dir": version.files,
                        "path": f"/p/{current.id}/{version.name}",
                        "global_form":
                            {
                                "method": "post",
                                "action": "",
                            },
                        "uuid": uuid.uuid4(),
                        "versions": current.versions.all(),
                        "version": version,
                        "title": f"edit {current.name}"
                    }
                )
        else:
            return HttpResponseForbidden("Edit not allowed")
    return HttpResponseNotAllowed(["GET", "POST"])


def hub(request):
    return redirect("/s/project?query=")