from django.contrib import admin
from django.urls import path
from .views import HomeView, AboutView, ClassesView, ContactView, ScheduleView, TrainerView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about", AboutView.as_view(), name="about"),
    path("classes", ClassesView.as_view(), name="classes"),
    path("contact", ContactView.as_view(), name="contact"),
    path("schedule", ScheduleView.as_view(), name="schedule"),
    path("trainer", TrainerView.as_view(), name="trainer"),

]