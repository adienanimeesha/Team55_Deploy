"""API serializers for Timetable and Reminders"""
from rest_framework import serializers
from .models import Timetable, ClassSession, Reminder


class ClassSessionSerializer(serializers.ModelSerializer):
    course_display = serializers.SerializerMethodField()
    reminder_status = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassSession
        fields = [
            'id',
            'course_code',
            'course_name',
            'session_type',
            'room_number',
            'building',
            'start_time',
            'end_time',
            'estimated_travel_time_minutes',
            'reminder_time',
            'course_display',
            'reminder_status',
        ]
    
    def get_course_display(self, obj):
        """Returns formatted course display"""
        return f"{obj.course_code} ({obj.session_type})"
    
    def get_reminder_status(self, obj):
        """Returns reminder status"""
        try:
            reminder = obj.reminder
            if reminder.is_dismissed:
                return 'dismissed'
            elif reminder.reminder_sent_at:
                return 'sent'
            else:
                return 'pending'
        except Reminder.DoesNotExist:
            return 'no_reminder'


class TimetableSerializer(serializers.ModelSerializer):
    classes = ClassSessionSerializer(many=True, read_only=True)
    class_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Timetable
        fields = [
            'user',
            'ics_file_name',
            'imported_at',
            'semester',
            'classes',
            'class_count',
        ]
    
    def get_class_count(self, obj):
        return obj.classes.count()


class ReminderSerializer(serializers.ModelSerializer):
    class_session = ClassSessionSerializer(read_only=True)
    
    class Meta:
        model = Reminder
        fields = [
            'id',
            'class_session',
            'is_dismissed',
            'reminder_sent_at',
            'user_dismissed_at',
            'created_at',
        ]


class IcsUploadSerializer(serializers.Serializer):
    """Serializer for uploading .ics file"""
    ics_file = serializers.FileField()
    semester = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_ics_file(self, value):
        """Validate that file has .ics extension"""
        if not value.name.endswith('.ics'):
            raise serializers.ValidationError("File must have .ics extension")
        return value
