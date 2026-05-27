from django.contrib import admin
from .models import Node, Edge, Timetable, ClassSession, Reminder


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'floor', 'label', 'type')
    list_filter = ('building', 'floor', 'type')
    search_fields = ('id', 'label')


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('from_node_id', 'to_node_id', 'weight')
    search_fields = ('from_node_id', 'to_node_id')


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('user', 'semester', 'imported_at')
    list_filter = ('semester', 'imported_at')
    search_fields = ('user__username',)


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'session_type', 'building', 'room_number', 'start_time', 'reminder_time')
    list_filter = ('building', 'start_time', 'session_type')
    search_fields = ('course_code', 'room_number')
    readonly_fields = ('reminder_time',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('class_session', 'is_dismissed', 'reminder_sent_at', 'created_at')
    list_filter = ('is_dismissed', 'created_at')
    search_fields = ('class_session__course_code',)

