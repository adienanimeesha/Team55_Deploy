# Smart Departure Reminders - Backend Implementation Summary

## ✅ What's Been Built

A complete Django REST API backend for smart class reminders that:
1. Parses `.ics` files from my.UQ timetables
2. Calculates optimal reminder times based on travel distance
3. Provides real-time reminder data to mobile frontend
4. Tracks reminder status and user dismissals

---

## 🏗️ Architecture Overview

```
User's Timetable (.ics)
       ↓
   [.ics Parser]
       ↓
   [Django Models]
  ├─ Timetable (user's schedule)
  ├─ ClassSession (individual class + location)
  └─ Reminder (notification state)
       ↓
   [REST API Endpoints]
       ↓
   [Mobile PWA Frontend]
```

---

## 📦 Models

### **Timetable**
Stores a user's complete timetable imported from `.ics` file.

```python
- user (OneToOne): Link to Django User
- ics_file_name: Name of uploaded file
- imported_at: When timetable was uploaded
- semester: e.g., "Semester 1 2026"
```

### **ClassSession**
Individual class with location and automatic reminder timing.

```python
- timetable (ForeignKey): Parent timetable
- course_code: e.g., "COMP4702"
- course_name: Full course name
- session_type: "Lecture", "Lab", "Tutorial"
- room_number: e.g., "315"
- building: e.g., "Building 69"
- start_time: Class start time
- end_time: Class end time
- estimated_travel_time_minutes: Time to walk from previous location
- reminder_time: AUTO-CALCULATED (class_time - travel - 5min_buffer)
```

**Example:**
- ECON2300 Lab: 10:00 AM in Building 69
- COMP4702 Lecture: 12:00 PM in Building 63 (8 min walk away)
- Travel + buffer: 8 min + 5 min = 13 minutes
- **Reminder sent at: 11:47 AM**

### **Reminder**
Tracks notification state for each class.

```python
- class_session (OneToOne): Link to class
- is_dismissed: User dismissed notification?
- reminder_sent_at: When notification was sent
- user_dismissed_at: When user dismissed it
- created_at: When reminder was created
```

---

## 🔌 REST API Endpoints

All endpoints require authentication (session or token-based).

### **Base URL**
```
http://localhost:8000/api/timetable/
```

### **1. Upload Timetable**
```
POST /upload-timetable/
```
Upload an `.ics` file and parse it into the system.

**Request:**
```bash
curl -X POST http://localhost:8000/api/timetable/upload-timetable/ \
  -H "Content-Type: multipart/form-data" \
  -F "ics_file=@data/test_timetable.ics" \
  -F "semester=Semester 1 2026"
```

**Response (201 Created):**
```json
{
  "message": "Successfully imported 2 classes",
  "timetable": {
    "user": 1,
    "semester": "Semester 1 2026",
    "class_count": 2,
    "classes": [...]
  }
}
```

---

### **2. Get My Timetable**
```
GET /my-timetable/
```
Retrieve full timetable with all classes and reminder status.

**Response:**
```json
{
  "user": 1,
  "semester": "Semester 1 2026",
  "class_count": 2,
  "classes": [
    {
      "id": "uuid-xxx",
      "course_code": "ECON2300",
      "course_name": "ECON2300 Lab",
      "session_type": "Lab",
      "room_number": "315",
      "building": "Building 69",
      "start_time": "2026-05-26T10:00:00Z",
      "end_time": "2026-05-26T12:00:00Z",
      "estimated_travel_time_minutes": 8,
      "reminder_time": "2026-05-26T09:47:00Z",
      "course_display": "ECON2300 (Lab)",
      "reminder_status": "pending"
    },
    {
      "id": "uuid-yyy",
      "course_code": "COMP4702",
      "course_name": "COMP4702 Lecture",
      "session_type": "Lecture",
      "room_number": "358",
      "building": "Building 63",
      "start_time": "2026-05-26T12:00:00Z",
      "end_time": "2026-05-26T14:00:00Z",
      "estimated_travel_time_minutes": 8,
      "reminder_time": "2026-05-26T11:47:00Z",
      "course_display": "COMP4702 (Lecture)",
      "reminder_status": "pending"
    }
  ]
}
```

---

### **3. Get All Classes**
```
GET /all-classes/
```
List all classes in user's timetable.

**Response:**
```json
{
  "count": 2,
  "classes": [...]
}
```

---

### **4. Get Next Class**
```
GET /next-class/
```
Get the user's next upcoming class.

**Response:**
```json
{
  "next_class": {
    "id": "uuid-xxx",
    "course_code": "ECON2300",
    ...
  }
}
```

---

### **5. Get Upcoming Reminders**
```
GET /upcoming-reminders/?hours=24
```
Get all reminders that should be sent in the next N hours.

**Parameters:**
- `hours` (optional): Look-ahead time in hours (default: 24)

**Response:**
```json
{
  "count": 1,
  "reminders": [
    {
      "id": "reminder-uuid",
      "class_session": {...},
      "is_dismissed": false,
      "reminder_sent_at": null,
      "user_dismissed_at": null,
      "created_at": "2026-05-26T08:00:00Z"
    }
  ]
}
```

---

### **6. Dismiss Reminder**
```
POST /dismiss-reminder/
```
Mark a reminder as dismissed by the user.

**Request:**
```json
{
  "reminder_id": "reminder-uuid"
}
```

**Response:**
```json
{
  "message": "Reminder dismissed",
  "reminder": {
    "id": "reminder-uuid",
    "is_dismissed": true,
    "user_dismissed_at": "2026-05-26T08:15:00Z",
    ...
  }
}
```

---

## 🧠 How It Works

### **Parsing Flow**
1. User uploads `.ics` file → Parser extracts events
2. For each event:
   - Extract course code, room, building, time
   - Parse location string (e.g., "315 Building 69" → room=315, building="Building 69")
3. Calculate travel time between consecutive classes
4. Calculate reminder time = `class_start - travel_time - 5_min_buffer`
5. Create ClassSession and Reminder objects

### **Travel Time Logic**
Currently uses **dummy data** with realistic times between UQ buildings:

```python
B69 ↔ B63: 8 minutes
B69 ↔ B50: 5 minutes  
B63 ↔ B50: 7 minutes
Default: 10 minutes
```

**Future:** Can be replaced with:
- MazeMap API call
- Your existing pathfinding algorithm
- Geolocation-based calculation

### **Reminder Calculation Example**
```
Scenario: Student with 2 classes

Class 1: ECON2300 Lab
├─ Start: 10:00 AM
├─ Location: Building 69, Room 315
└─ Reminder Time: 9:47 AM

Class 2: COMP4702 Lecture  
├─ Start: 12:00 PM
├─ Location: Building 63, Room 358
├─ Travel from B69→B63: 8 minutes
├─ Buffer: 5 minutes
└─ Reminder Time: 11:47 AM (12:00 - 8min - 5min)
```

---

## 🧪 Testing

### **Generate Test Data**
```bash
python manage.py generate_test_ics
# Creates: data/test_timetable.ics
```

### **Test ICS File Contents**
```
ECON2300 Lab: 10:00 AM in Building 69 room 315
COMP4702 Lecture: 12:00 PM in Building 63 room 358
```

### **Manual Testing with cURL**

**1. Create a test user:**
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('testuser', 'test@example.com', 'password123')
```

**2. Login (get session cookie):**
```bash
curl -c cookies.txt -X POST http://localhost:8000/login/ \
  -d "username=testuser&password=password123"
```

**3. Upload timetable:**
```bash
curl -b cookies.txt -X POST http://localhost:8000/api/timetable/upload-timetable/ \
  -F "ics_file=@data/test_timetable.ics" \
  -F "semester=Test Semester"
```

**4. Check timetable:**
```bash
curl -b cookies.txt http://localhost:8000/api/timetable/my-timetable/
```

**5. Get upcoming reminders:**
```bash
curl -b cookies.txt "http://localhost:8000/api/timetable/upcoming-reminders/?hours=24"
```

---

## 📁 Project Structure

```
indoor_nav/
├── models.py                           # Timetable, ClassSession, Reminder models
├── views.py                            # API ViewSet with all endpoints
├── serializers.py                      # DRF serializers for JSON
├── ics_parser.py                       # .ics parsing logic
├── urls.py                             # API routing
├── admin.py                            # Django admin interface
├── migrations/
│   └── 0004_timetable_reminder_models.py  # New models migration
├── management/
│   └── commands/
│       └── generate_test_ics.py        # Test data generator
└── ...

mvp/
├── settings.py                         # Added REST_FRAMEWORK config
└── urls.py                             # Added /api/ route

requirements.txt                        # Updated with icalendar, etc.
API_DOCUMENTATION.md                    # Full API docs
SMART_REMINDERS_BACKEND_SUMMARY.md      # This file
```

---

## ⚙️ Configuration

### **Added to settings.py:**
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### **New packages in requirements.txt:**
- `djangorestframework` - REST API framework
- `icalendar` - .ics file parsing
- `python-dateutil` - Date/time utilities
- `celery` - Background task scheduling (ready for push notifications)

---

## 🚀 Next Steps: Frontend PWA

The backend is **complete and ready** for frontend consumption. Next phase should build:

1. **Frontend PWA (React/Vue)**
   - `.ics` upload form UI
   - Geolocation permission + location display
   - Notification UI component

2. **Service Worker + Web Push**
   - Background notifications
   - Handle reminder notifications
   - Offline map caching

3. **Celery Tasks** (optional)
   - Scheduled reminder dispatch
   - Notification queue management

4. **Enhanced Travel Time**
   - Replace dummy data with MazeMap API
   - Or use your existing pathfinding algorithm

---

## 🔍 API Testing Checklist

- [ ] Upload `.ics` file → Creates Timetable
- [ ] Parse course info → ClassSession with correct details
- [ ] Calculate reminder_time → 5min before class - travel
- [ ] Get timetable → Returns all classes
- [ ] Get upcoming reminders → Filters correctly
- [ ] Dismiss reminder → Marks is_dismissed=True
- [ ] Get next class → Returns closest upcoming

---

## 💡 Key Features

✅ **ICS Parsing** - Extracts course code, time, location from .ics files  
✅ **Smart Reminder Timing** - Calculates based on travel distance  
✅ **Travel Time Aware** - Knows distance between buildings  
✅ **Status Tracking** - Pending → Sent → Dismissed  
✅ **User Isolation** - Each user's timetable is private  
✅ **RESTful API** - Easy for frontend consumption  
✅ **Admin Interface** - Manage timetables in Django admin  
✅ **Test Data Generator** - Quick setup for development  

---

## 🐛 Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'icalendar'`
```bash
pip install icalendar
```

**Issue:** API returns 404
- Ensure user is authenticated
- Upload timetable first
- Check user exists in database

**Issue:** Reminder times seem wrong
- Check travel time calculation in `get_travel_time()`
- Update dummy travel times if needed
- Verify class start/end times are correct

---

## 📞 API Support

For detailed endpoint usage, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

All endpoints are at: `http://localhost:8000/api/timetable/`
