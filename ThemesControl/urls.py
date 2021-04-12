from django.urls import path
from . import views
from Search.views import search_themes
from django.shortcuts import redirect

urlpatterns = [
    path("<int:id>/", views.theme_by_id, name="theme_by_id"),
    path("", lambda r: redirect("/s/theme?query="), name="theme_hub"),
]