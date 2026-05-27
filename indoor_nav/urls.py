"""URL routing for indoor_nav app"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'timetable', views.TimetableViewSet, basename='timetable')

urlpatterns = router.urls
