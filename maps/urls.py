from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("building/<str:building_id>/", views.building_detail, name="building_detail"),
    path("reminders/", views.reminders, name="reminders"),
]