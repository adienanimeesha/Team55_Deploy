from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="onboarding", permanent=False)),
    path("building/<str:building_id>/", views.building_detail, name="building_detail"),
    path("reminders/", views.reminders, name="reminders"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("map/", views.home, name="home"),
]
