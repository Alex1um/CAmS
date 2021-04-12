from django.shortcuts import render, redirect
from ThemesControl.models import Theme
from ProjectControl.models import Project, Version


def fix_reqest(request, filters):
    flag = False
    if query := request.GET.getlist("query"):
        if len(query) > 1:
            request.GET.setlist("query", [query[-1]])
            flag = True
    for filter in filters:
        if temp := request.GET.getlist(filter):
            if len(temp) > 1:
                request.GET.setlist(filter, ["<" if temp[0] == ">" else ">"])
                flag = True
            elif temp[0] == "":
                request.GET.setlist(filter, ">")
                flag = True
    if flag:
        return request.GET.urlencode()


# Create your views here.
def search_themes(request):
    # So bad
    if not request.GET._mutable:
        request.GET._mutable = True
    if temp := fix_reqest(request, ["name"]):
        return redirect(request.path + "?" + temp)
    query = request.GET.get("query", "")
    if query:
        objs = Theme.objects.filter(name__contains=query)
    else:
        objs = Theme.objects.all()
    sort = {}
    temp = request.GET.get("name")
    if temp:
        sort["name"] = temp
        objs = objs.order_by("name")
        if temp == ">":
            objs = objs[::-1]
    themes = objs

    return render(request, "search\\search-themes.html",
                  {
                      "path": request.get_full_path(),
                      "themes": themes,
                      "query": query,
                      "sort": sort,
                      "page_type": "themes",
                      "title": "Find themes"
                  }
                  )


def search_projects(request):
    # So bad
    if not request.GET._mutable:
        request.GET._mutable = True
    if temp := fix_reqest(request, ["name", "version"]):
        return redirect(request.path + "?" + temp)
    query = request.GET.get("query", "")
    if query:
        objs = Project.objects.filter(name__contains=query)
    else:
        objs = Project.objects.all()

    sort = {}
    temp = request.GET.get("name")
    if temp:
        sort["name"] = temp
        objs = objs.order_by("name")
        if temp == "<":
            objs = objs[::-1]
    temp = request.GET.get("theme")
    if temp:
        if theme := Theme.objects.get(id=temp):
            sort["theme"] = temp
            objs = objs.filter(theme=theme)
    projects = map(lambda obj: (obj, obj.versions.first().name), objs)

    return render(request, "search\\search-projects.html",
                  {
                      "path": request.get_full_path(),
                      "projects": projects,
                      "query": query,
                      "sort": sort,
                      "page_type": "projects",
                      "title": "Find projects"
                  }
                  )
