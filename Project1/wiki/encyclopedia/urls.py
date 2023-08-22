from django.urls import path

from . import views

# app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("css", views.css, name="css"),
    path("django", views.django, name="django"),
    path("git", views.git, name="git"),
    path("html", views.html, name="html"),
    path("python", views.python, name="python")
]
