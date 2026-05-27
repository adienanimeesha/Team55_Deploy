"""
Management command to generate dummy ICS file for testing.
Usage: python manage.py generate_test_ics
"""
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os


class Command(BaseCommand):
    help = 'Generate a test ICS file for timetable testing'

    def handle(self, *args, **options):
        # Create dummy ICS content
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//My UQ//Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:econ2300-lab@uq.edu.au
DTSTART:20260526T100000Z
DTEND:20260526T120000Z
SUMMARY:ECON2300 Lab
LOCATION:315 Building 69
DESCRIPTION:Economics Lab Session
END:VEVENT
BEGIN:VEVENT
UID:comp4702@uq.edu.au
DTSTART:20260526T120000Z
DTEND:20260526T140000Z
SUMMARY:COMP4702 Lecture
LOCATION:358 Building 63
DESCRIPTION:Machine Learning Lecture
END:VEVENT
END:VCALENDAR"""

        # Write to file
        file_path = 'data/test_timetable.ics'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(ics_content)
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Test ICS file created at {file_path}')
        )
        self.stdout.write('You can upload this file via the API:')
        self.stdout.write('  POST /api/timetable/upload-timetable/')
