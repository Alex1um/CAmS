from django.shortcuts import render
from .models import Theme
from django.db.models import ObjectDoesNotExist


# Create your views here.
def theme_by_id(request, id):
    try:
        theme = Theme.objects.get(id=id)
        projects = theme.projects.all()
        return render(
            request,
            "themes\\theme-one.html",
            {
                "title": theme.name,
                "page_type": "theme",
                "theme": theme,
                "projects": ((p, p.versions.first().name) for p in projects),
            }
        )
    except ObjectDoesNotExist:
        return render(request,
                      "misc\\notexist.html",
                      {
                          "title": "Wrong address"
                      }
                      )


def themes_hub(request):
    return render(request,
                  "themes\\themes-hub.html",
                  {
                      "title": "Themes",
                      "page_type": "themes",
                      "themes": Theme.objects.all(),
                      "themes_featured": Theme.objects.all(),
                  }
                  )