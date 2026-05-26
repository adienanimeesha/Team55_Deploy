from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Node(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    building = models.CharField(max_length=20, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=200, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    uq_maps_identifier = models.CharField(max_length=100, blank=True)
    poi_id = models.IntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.label or self.id


class Edge(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_from')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_to')
    weight = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.from_node_id} → {self.to_node_id}"


class Timetable(models.Model):
    """Stores a user's timetable imported from .ics file"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='timetable')
    ics_file_name = models.CharField(max_length=255, default='timetable.ics')
    imported_at = models.DateTimeField(auto_now=True)
    semester = models.CharField(max_length=50, blank=True, help_text="e.g., 'Semester 1 2024'")

    def __str__(self):
        return f"Timetable for {self.user.username}"


class ClassSession(models.Model):
    """A single class session from the user's timetable"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='classes')
    
    # Course info
    course_code = models.CharField(max_length=50)  # e.g., 'COMP4702', 'ECON2300'
    course_name = models.CharField(max_length=255, blank=True)
    session_type = models.CharField(max_length=50, blank=True)  # e.g., 'Lecture', 'Lab', 'Tutorial'
    
    # Location
    room_number = models.CharField(max_length=100)  # e.g., '358', '315'
    building = models.CharField(max_length=50)  # e.g., 'Building 63', 'Building 69'
    
    # Timing
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Travel info
    estimated_travel_time_minutes = models.IntegerField(null=True, blank=True, help_text="Minutes from previous location")
    reminder_time = models.DateTimeField(null=True, blank=True, help_text="When to send reminder (auto-calculated)")

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.course_code} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Reminder(models.Model):
    """Stores reminder state for each class"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_session = models.OneToOneField(ClassSession, on_delete=models.CASCADE, related_name='reminder')
    
    is_dismissed = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)
    user_dismissed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Dismissed" if self.is_dismissed else "Pending"
        return f"Reminder for {self.class_session.course_code} - {status}"
