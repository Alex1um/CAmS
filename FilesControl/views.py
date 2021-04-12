from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from ProjectControl.models import Project, Version, Dependence


# Create your views here.
def watch_file(request, dir):
    splitted = dir.split("/")
    project = Project.objects.get(id=int(splitted[0]))
    version = splitted[1]
    files = project.files.get(version=version)
    to_file = splitted[2:]
    return HttpResponseNotAllowed("no")


def make_dependence(request, pid):
    project = Project.objects.get(id=pid)
    version = project.versions.first()
    files = version.files[0]
    for p in request.POST.keys():
        if p != "csrfmiddlewaretoken" and (p := int(p)) != project.id:
            temp = Project.objects.get(id=p)
            fd: Version = temp.versions.first()
            fd.files[0]["files"].append(files)
            Dependence.objects.create(
                project=temp,
                files=files,
                project_dependency=project,
                project_dependency_version=version,
            ).save()
            fd.save()
    return redirect(f"/p/{project.id}")