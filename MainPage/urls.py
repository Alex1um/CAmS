from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartPage, "start_page"),
]
