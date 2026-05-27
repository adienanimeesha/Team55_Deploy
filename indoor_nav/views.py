from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Timetable, ClassSession, Reminder
from .serializers import (
    TimetableSerializer,
    ClassSessionSerializer,
    ReminderSerializer,
    IcsUploadSerializer,
)
from .ics_parser import parse_ics_file, get_upcoming_reminders


class TimetableViewSet(viewsets.ViewSet):
    """
    API endpoint for managing user timetables and reminders.
    Public access - no authentication required.
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='my-timetable')
    def my_timetable(self, request):
        """Get the current user's timetable"""
        user = self._get_guest_user()
        try:
            timetable = user.timetable
            serializer = TimetableSerializer(timetable)
            return Response(serializer.data)
        except Timetable.DoesNotExist:
            return Response(
                {'error': 'No timetable found. Please upload an .ics file first.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def _get_guest_user(self):
        """Get or create a guest user for this session"""
        from django.contrib.auth.models import User
        guest_user, _ = User.objects.get_or_create(username='guest_user')
        return guest_user

    @action(detail=False, methods=['post'], url_path='upload-timetable')
    def upload_timetable(self, request):
        """Upload and parse an .ics file"""
        serializer = IcsUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = self._get_guest_user()
        ics_file = serializer.validated_data['ics_file']
        semester = serializer.validated_data.get('semester', '')
        
        try:
            # Read file content
            ics_content = ics_file.read()
            
            # Parse ICS file
            result = parse_ics_file(ics_content, user, semester)
            
            if result['errors']:
                return Response(
                    {
                        'created': len(result['created']),
                        'errors': result['errors'],
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Return updated timetable
            timetable = user.timetable
            timetable_serializer = TimetableSerializer(timetable)
            
            return Response(
                {
                    'message': f'Successfully imported {len(result["created"])} classes',
                    'timetable': timetable_serializer.data,
                },
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': f'Failed to process file: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='upcoming-reminders')
    def upcoming_reminders(self, request):
        """Get reminders for the next 24 hours"""
        user = self._get_guest_user()
        hours = request.query_params.get('hours', 24)
        try:
            hours = int(hours)
        except ValueError:
            hours = 24
        
        reminders = get_upcoming_reminders(user, hours_ahead=hours)
        serializer = ReminderSerializer(reminders, many=True)
        
        return Response({
            'count': reminders.count(),
            'reminders': serializer.data,
        })

    @action(detail=False, methods=['get'], url_path='all-classes')
    def all_classes(self, request):
        """Get all classes from user's timetable"""
        user = self._get_guest_user()
        try:
            timetable = user.timetable
            classes = timetable.classes.all()
            serializer = ClassSessionSerializer(classes, many=True)
            return Response({
                'count': classes.count(),
                'classes': serializer.data,
            })
        except Timetable.DoesNotExist:
            return Response(
                {'error': 'No timetable found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], url_path='dismiss-reminder')
    def dismiss_reminder(self, request):
        """Mark a reminder as dismissed"""
        reminder_id = request.data.get('reminder_id')
        
        if not reminder_id:
            return Response(
                {'error': 'reminder_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reminder = Reminder.objects.get(id=reminder_id)
            
            reminder.is_dismissed = True
            reminder.user_dismissed_at = timezone.now()
            reminder.save()
            
            serializer = ReminderSerializer(reminder)
            return Response({
                'message': 'Reminder dismissed',
                'reminder': serializer.data,
            })
        except Reminder.DoesNotExist:
            return Response(
                {'error': 'Reminder not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='next-class')
    def next_class(self, request):
        """Get the next upcoming class"""
        user = self._get_guest_user()
        try:
            timetable = user.timetable
            next_class = timetable.classes.filter(
                start_time__gte=timezone.now()
            ).first()
            
            if not next_class:
                return Response({
                    'next_class': None,
                    'message': 'No upcoming classes',
                })
            
            serializer = ClassSessionSerializer(next_class)
            return Response({
                'next_class': serializer.data,
            })
        except Timetable.DoesNotExist:
            return Response(
                {'error': 'No timetable found'},
                status=status.HTTP_404_NOT_FOUND
            )

