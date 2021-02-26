from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from ProjectControl.models import Project, FileDirectory, Dependence


# Create your views here.
def watch_file(request, dir):
    splitted = dir.split("/")
    print(splitted)
    project = Project.objects.get(id=int(splitted[0]))
    version = splitted[1]
    files = project.files.get(version=version)
    to_file = splitted[2:]
    return HttpResponseNotAllowed("no")


def make_dependence(request, pid):
    project = Project.objects.get(id=pid)
    files = project.files.last()
    for p in request.POST.keys():
        if p != "csrfmiddlewaretoken" and (p := int(p)) != project:
            temp = Project.objects.get(id=p)
            fd: FileDirectory = temp.files.last()
            fd.files[0]["files"].append(files.files[0])
            Dependence.objects.create(
                project=project,
                files=files,
                project_dependency=temp,
            ).save()
            fd.save()
    return redirect(f"/p/{project.id}")