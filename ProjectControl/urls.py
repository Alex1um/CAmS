from django.urls import path
from . import views
from FilesControl import views as fileviews


urlpatterns = [
    path("<int:id>", views.view_project, name='project_view'),
    path("edit/<int:id>", views.edit_project, name="project_edit"),
    path("", views.hub, name="projects_hub"),
    path("mkdep/<int:pid>", fileviews.make_dependence, name="make_dependence"),
    path("<path:dir>", fileviews.watch_file, name="project_file_view"),
]