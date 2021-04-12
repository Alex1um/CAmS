from django.urls import path
from . import views

urlpatterns = [
    path('theme', views.search_themes, name="search_theme"),
    path('project', views.search_projects, name="search_project")
]