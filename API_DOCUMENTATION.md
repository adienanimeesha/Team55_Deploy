# Smart Departure Reminders API

## Overview
This API manages user timetables imported from `.ics` files and provides intelligent departure reminders based on class locations and travel times.

## Authentication
All endpoints require session authentication. User must be logged in.

## Base URL
```
http://localhost:8000/api/timetable/
```

## Endpoints

### 1. Upload Timetable
**POST** `/upload-timetable/`

Upload an `.ics` file from my.UQ to import your timetable.

**Parameters:**
- `ics_file` (required): .ics file from my.UQ
- `semester` (optional): Semester label (e.g., "Semester 1 2024")

**Example:**
```bash
curl -X POST http://localhost:8000/api/timetable/upload-timetable/ \
  -H "Content-Type: multipart/form-data" \
  -F "ics_file=@timetable.ics" \
  -F "semester=Semester 1 2026"
```

**Response:**
```json
{
  "message": "Successfully imported 2 classes",
  "timetable": {
    "user": 1,
    "ics_file_name": "timetable.ics",
    "imported_at": "2026-05-26T12:00:00Z",
    "semester": "Semester 1 2026",
    "classes": [...],
    "class_count": 2
  }
}
```

---

### 2. Get My Timetable
**GET** `/my-timetable/`

Retrieve your current timetable with all classes and reminders.

**Example:**
```bash
curl http://localhost:8000/api/timetable/my-timetable/
```

**Response:**
```json
{
  "user": 1,
  "semester": "Semester 1 2026",
  "class_count": 2,
  "classes": [
    {
      "id": "uuid-1",
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
      "id": "uuid-2",
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

### 3. Get Upcoming Reminders
**GET** `/upcoming-reminders/?hours=24`

Get reminders that should be sent in the next N hours.

**Parameters:**
- `hours` (optional): Look ahead time in hours (default: 24)

**Example:**
```bash
curl "http://localhost:8000/api/timetable/upcoming-reminders/?hours=24"
```

**Response:**
```json
{
  "count": 1,
  "reminders": [
    {
      "id": "reminder-uuid",
      "class_session": {
        "id": "class-uuid",
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
      "is_dismissed": false,
      "reminder_sent_at": null,
      "user_dismissed_at": null,
      "created_at": "2026-05-26T08:00:00Z"
    }
  ]
}
```

---

### 4. Get All Classes
**GET** `/all-classes/`

Get all classes from your timetable.

**Example:**
```bash
curl http://localhost:8000/api/timetable/all-classes/
```

**Response:**
```json
{
  "count": 2,
  "classes": [...]
}
```

---

### 5. Get Next Class
**GET** `/next-class/`

Get your next upcoming class.

**Example:**
```bash
curl http://localhost:8000/api/timetable/next-class/
```

**Response:**
```json
{
  "next_class": {
    "id": "class-uuid",
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
  }
}
```

---

### 6. Dismiss Reminder
**POST** `/dismiss-reminder/`

Mark a reminder as dismissed by the user.

**Parameters:**
- `reminder_id` (required): UUID of the reminder to dismiss

**Example:**
```bash
curl -X POST http://localhost:8000/api/timetable/dismiss-reminder/ \
  -H "Content-Type: application/json" \
  -d '{"reminder_id": "reminder-uuid"}'
```

**Response:**
```json
{
  "message": "Reminder dismissed",
  "reminder": {
    "id": "reminder-uuid",
    "class_session": {...},
    "is_dismissed": true,
    "reminder_sent_at": null,
    "user_dismissed_at": "2026-05-26T08:15:00Z",
    "created_at": "2026-05-26T08:00:00Z"
  }
}
```

---

## Data Flow

### 1. Upload Timetable
- User uploads `.ics` file → Parser extracts course info, times, locations
- Travel time calculated (current: dummy data, fallback: MazeMap API)
- Reminder time = class_time - travel_time - 5min_buffer
- Example: ECON2300 at 10:00 in B69 → COMP4702 at 12:00 in B63
  - Travel: 8 minutes
  - Reminder: 12:00 - 8min - 5min = 11:47 AM

### 2. Reminder Workflow
- Upcoming reminders fetched every few minutes by frontend
- Send notification: "Time to head to ECON2300 in Building 69 (5 min walk)"
- User can dismiss or navigate
- Status tracked: pending → sent → dismissed

## Travel Time Calculation

Currently using dummy data (realistic times between buildings):
- B69 ↔ B63: 8 minutes
- B69 ↔ B50: 5 minutes
- B63 ↔ B50: 7 minutes

**Future:** Use MazeMap API or pathfinding algorithm for actual routes.

## Testing

### Generate Test ICS
```bash
python manage.py generate_test_ics
```

This creates `data/test_timetable.ics` with:
- ECON2300 Lab at 10:00 in Building 69 room 315
- COMP4702 Lecture at 12:00 in Building 63 room 358

### Upload Test File
```bash
curl -X POST http://localhost:8000/api/timetable/upload-timetable/ \
  -H "Content-Type: multipart/form-data" \
  -F "ics_file=@data/test_timetable.ics" \
  -F "semester=Test Semester"
```

## Error Handling

| Status | Error | Solution |
|--------|-------|----------|
| 404 | No timetable found | Upload .ics file first |
| 400 | File must have .ics extension | Use valid .ics file |
| 403 | Unauthorized | Check authentication |
| 500 | Failed to process file | Check file format |

## Next Steps

1. **Frontend PWA**: Implement geolocation, notifications, UI
2. **Background Tasks**: Celery for scheduled reminder dispatch
3. **MazeMap Integration**: Real travel time calculation
4. **Web Push**: Native browser notifications
5. **Offline Caching**: Service Worker for offline maps
