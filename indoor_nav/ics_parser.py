"""Parse .ics files and extract class information"""
import re
from datetime import datetime, timedelta
from icalendar import Calendar
from .models import ClassSession, Timetable, Reminder


def parse_room_and_building(location_str):
    """
    Extract room number and building from location string.
    Examples:
    - "358 Building 63" → ('358', 'Building 63')
    - "Building 69 315" → ('315', 'Building 69')
    - "B50-S201" → ('S201', 'Building 50')
    """
    if not location_str:
        return None, None
    
    location = location_str.strip()
    
    # Pattern 1: "358 Building 63" or "Building 63 358"
    match = re.search(r'(\d{2,3})\s+Building\s+(\d{2})', location)
    if match:
        room = match.group(1)
        building_num = match.group(2)
        return room, f'Building {building_num}'
    
    match = re.search(r'Building\s+(\d{2})\s+(\d{2,3})', location)
    if match:
        building_num = match.group(1)
        room = match.group(2)
        return room, f'Building {building_num}'
    
    # Pattern 2: "B50-S201" format
    match = re.search(r'B(\d{2})-([A-Z]\d{3})', location)
    if match:
        building_num = match.group(1)
        room = match.group(2)
        return room, f'Building {building_num}'
    
    # Fallback: return first number as room
    numbers = re.findall(r'\d+', location)
    if numbers:
        return numbers[0], location
    
    return None, location


def calculate_reminder_time(class_start, travel_time_minutes=15, reminder_buffer_minutes=5):
    """
    Calculate when to send reminder.
    Reminder time = class start - travel time - buffer
    E.g., class at 2pm, 8min travel, 5min buffer → remind at 1:47pm
    """
    return class_start - timedelta(minutes=travel_time_minutes + reminder_buffer_minutes)


def get_travel_time(from_building, to_building):
    """
    Get estimated travel time between buildings.
    For now, use dummy data. Later can call MazeMap API.
    
    Returns travel time in minutes.
    """
    # Dummy travel times between buildings
    travel_times = {
        ('Building 69', 'Building 63'): 8,
        ('Building 63', 'Building 69'): 8,
        ('Building 69', 'Building 50'): 5,
        ('Building 50', 'Building 69'): 5,
        ('Building 63', 'Building 50'): 7,
        ('Building 50', 'Building 63'): 7,
    }
    
    key = (from_building, to_building)
    reverse_key = (to_building, from_building)
    
    if key in travel_times:
        return travel_times[key]
    elif reverse_key in travel_times:
        return travel_times[reverse_key]
    else:
        # Default to 10 minutes if not found
        return 10


def parse_ics_file(ics_file_content, user, semester=""):
    """
    Parse an .ics file and create ClassSession objects.
    
    Args:
        ics_file_content: Binary content of .ics file
        user: Django User object
        semester: Optional semester string
    
    Returns:
        dict with keys 'created', 'errors'
    """
    try:
        cal = Calendar.from_ical(ics_file_content)
    except Exception as e:
        return {'created': [], 'errors': [f'Failed to parse ICS file: {str(e)}']}
    
    # Get or create timetable
    timetable, _ = Timetable.objects.get_or_create(user=user)
    timetable.semester = semester
    timetable.save()
    
    # Clear existing classes
    timetable.classes.all().delete()
    
    created = []
    errors = []
    previous_building = None
    
    for component in cal.walk():
        if component.name == 'VEVENT':
            try:
                # Extract event details
                summary = str(component.get('summary', ''))
                location = str(component.get('location', ''))
                dtstart = component.get('dtstart')
                dtend = component.get('dtend')
                
                if not dtstart or not dtend:
                    continue
                
                start_time = dtstart.dt if hasattr(dtstart.dt, 'year') else dtstart.dt
                end_time = dtend.dt if hasattr(dtend.dt, 'year') else dtend.dt
                
                # Convert to datetime if date-only
                if not isinstance(start_time, datetime):
                    start_time = datetime.combine(start_time, datetime.min.time())
                if not isinstance(end_time, datetime):
                    end_time = datetime.combine(end_time, datetime.min.time())
                
                # Parse course code and session type
                # Expected format: "COMP4702 Lecture" or "ECON2300 Lab"
                parts = summary.split()
                course_code = parts[0] if parts else 'UNKNOWN'
                session_type = ' '.join(parts[1:]) if len(parts) > 1 else ''
                
                # Parse room and building
                room_number, building = parse_room_and_building(location)
                if not building:
                    building = 'Unknown Building'
                
                # Calculate travel time
                travel_time = 0
                if previous_building and building != previous_building:
                    travel_time = get_travel_time(previous_building, building)
                
                previous_building = building
                
                # Calculate reminder time (5 min buffer)
                reminder_time = calculate_reminder_time(
                    start_time,
                    travel_time_minutes=travel_time,
                    reminder_buffer_minutes=5
                )
                
                # Create ClassSession
                class_session = ClassSession.objects.create(
                    timetable=timetable,
                    course_code=course_code,
                    course_name=summary,
                    session_type=session_type,
                    room_number=room_number or 'TBA',
                    building=building,
                    start_time=start_time,
                    end_time=end_time,
                    estimated_travel_time_minutes=travel_time,
                    reminder_time=reminder_time,
                )
                
                # Create Reminder
                Reminder.objects.create(class_session=class_session)
                
                created.append(class_session)
                
            except Exception as e:
                errors.append(f'Error parsing event: {str(e)}')
    
    return {
        'created': created,
        'errors': errors,
    }


def get_upcoming_reminders(user, hours_ahead=24):
    """
    Get reminders that should be sent in the next N hours.
    """
    from django.utils import timezone
    
    now = timezone.now()
    future = now + timedelta(hours=hours_ahead)
    
    try:
        timetable = user.timetable
        reminders = Reminder.objects.filter(
            class_session__timetable=timetable,
            class_session__reminder_time__gte=now,
            class_session__reminder_time__lte=future,
            is_dismissed=False,
            reminder_sent_at__isnull=True,
        ).select_related('class_session')
        
        return reminders
    except Timetable.DoesNotExist:
        return Reminder.objects.none()
