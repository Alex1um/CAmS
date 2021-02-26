from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.theme_by_id, name="theme_by_id"),
    path("", views.themes_hub, name="theme_hub"),
]