from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_public, name="home_public"),
]