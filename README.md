# Event Management System API

A comprehensive FastAPI-based event management system that allows users to manage events, speakers, user registrations, and attendance tracking.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
  - [Users](#users)
  - [Events](#events)
  - [Speakers](#speakers)
  - [Registrations](#registrations)
- [Data Models](#data-models)
- [Business Logic](#business-logic)
- [Error Handling](#error-handling)

## Features

- **User Management**: Create, read, update, and soft-delete users
- **Event Management**: Create and manage events with location
- **Speaker Management**: Manage speakers with topic-based searching
- **Registration System**: Register users for events with validation
- **Attendance Tracking**: Mark and track event attendance
- **Search Functionality**: Search users by name, speakers by name/topic
- **Data Validation**: Comprehensive input validation using Pydantic
- **Error Handling**: Custom HTTP exception handling
- **CORS Support**: Cross-origin resource sharing enabled

## Tech Stack

- **Backend Framework**: FastAPI
- **Data Validation**: Pydantic
- **Data Storage**: In-memory storage (lists)
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Python Version**: Python 3.7+

## Project Structure

```
altschool_second_semester_exam/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # In-memory data storage
│   ├── models.py               # Data models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py             # User endpoints
│   │   ├── event.py            # Event endpoints
│   │   ├── speaker.py          # Speaker endpoints
│   │   └── registration.py     # Registration endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── event.py            # Event Pydantic schemas
│   │   └── speaker.py          # Speaker Pydantic schemas
│   └── services/
│       ├── __init__.py
│       ├── user.py             # User business logic
│       ├── event.py            # Event business logic
│       └── speaker.py          # Speaker business logic
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- uv (Python package and project manager)

### Setup Instructions

1. **Install uv** (if not already installed)
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Alternative: using pip
   pip install uv
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd altschool_second_semester_exam
   ```

3. **Create project and install dependencies**
   ```bash
   # Initialize uv project (if pyproject.toml doesn't exist)
   uv init
   
   # Add dependencies
   uv add fastapi uvicorn pydantic email-validator
   ```

4. **Sync dependencies** (ensures all dependencies are installed)
   ```bash
   uv sync
   ```

## Running the Application

### Development Server

1. **Start the FastAPI development server using uv**
   ```bash
   uv run fastapi dev
   ```

2. **Alternative method with custom host and port**
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Run with Python module**
   ```bash
   uv run python -m uvicorn app.main:app --reload
   ```

### Production Server

For production deployment:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using uv Scripts (Optional)

You can also add scripts to your `pyproject.toml` file for easier management:

```toml
[project.scripts]
dev = "uvicorn app.main:app --reload"
start = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

Then run:
```bash
# Development
uv run dev

# Production
uv run start
```

### Accessing the Application

- **API Base URL**: `http://localhost:8000`
- **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI JSON Schema**: `http://localhost:8000/openapi.json`

## API Documentation

The API automatically generates comprehensive documentation using FastAPI's built-in OpenAPI support. Visit `/docs` for an interactive interface where you can test all endpoints.

## API Endpoints

### Users

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/users/` | Create a new user | `UserCreate` |
| `GET` | `/users/` | Get all users (with active filter) | Query: `active_only=true` |
| `GET` | `/users/attended-events` | Get users who attended events | None |
| `GET` | `/users/search` | Search users by name | Query: `name` |
| `GET` | `/users/email/{email}` | Get user by email | None |
| `GET` | `/users/{user_id}` | Get user by ID | None |
| `PATCH` | `/users/{user_id}` | Update user | `UserUpdate` |
| `PUT` | `/users/{user_id}` | Soft delete user | None |

### Events

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/events/` | Create a new event | `EventCreate` |
| `GET` | `/events/` | Get all events | Query: `open_only=true`, `location` |
| `GET` | `/events/{event_id}` | Get event by ID | None |
| `GET` | `/events/{event_id}/attendees` | Get event attendees | None |
| `PUT` | `/events/{event_id}` | Update event | `EventUpdate` |
| `PUT` | `/events/{event_id}` | Close event | None |

### Speakers

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/speakers/` | Create a new speaker | `SpeakerCreate` |
| `GET` | `/speakers/` | Get all speakers | None |
| `GET` | `/speakers/search/name` | Search speakers by name | Query: `name` |
| `GET` | `/speakers/search/topic` | Search speakers by topic | Query: `topic` |
| `GET` | `/speakers/{speaker_id}` | Get speaker by ID | None |
| `PUT` | `/speakers/{speaker_id}` | Update speaker | `SpeakerUpdate` |
| `DELETE` | `/speakers/{speaker_id}` | Delete speaker | None |

### Registrations

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/registrations/` | Get all registrations | None |
| `GET` | `/registrations/user/{user_id}` | Get user's registrations | None |
| `POST` | `/registrations/{event_id}/register/{user_id}` | Register user for event | None |
| `PUT` | `/registrations/{registration_id}/attendance` | Mark attendance | None |

## Data Models

### User
```python
class User:
    id: int
    name: str
    email: str
    is_active: bool = True
```

### Event
```python
class Event:
    id: int
    title: str
    location: str
    event_date: date
    is_open: bool = True
```

### Speaker
```python
class Speaker:
    id: int
    name: str
    topic: str
```

### Registration
```python
class Registration:
    id: int
    user_id: int
    event_id: int
    registration_date: date
    attended: bool = False
```

## Business Logic

### User Registration for Events

The system enforces several business rules when registering users for events:

1. **User Validation**:
   - User must exist in the system
   - User must be active (`is_active = True`)

2. **Event Validation**:
   - Event must exist
   - Event must be open (`is_open = True`)

3. **Duplicate Prevention**:
   - Users cannot register for the same event twice

### Data Integrity

- **Email Uniqueness**: User emails must be unique across the system
- **Soft Deletion**: Users and events are soft-deleted (marked as inactive/closed) rather than permanently removed
- **Attendance Tracking**: Registration records track whether users actually attended events

## Error Handling

The API implements comprehensive error handling:

- **404 Not Found**: When requested resources don't exist
- **400 Bad Request**: For validation errors and business rule violations
- **Detailed Error Messages**: All errors include descriptive messages

### Example Error Response
```json
{
  "error": {
    "detail": "User with this email already exists",
    "type": "http_error"
  }
}
```

## Sample API Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john.doe@example.com"
     }'
```

### Create an Event
```bash
curl -X POST "http://localhost:8000/events/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Tech Conference 2024",
       "location": "Lagos, Nigeria",
       "date": "2024-12-01"
     }'
```

### Register User for Event
```bash
curl -X POST "http://localhost:8000/registrations/1/register/1"
```

## Default Data

The system comes pre-populated with sample speakers:

1. **Israel Boluwatife** - Full-Stack Web Development
2. **Babatunde Taiwo** - Cloud Architecture  
3. **Frank Felix** - Machine Learning and AI

## Development Notes

- **In-Memory Storage**: Current implementation uses in-memory lists for data storage
- **Data Persistence**: Data is not persisted between application restarts


---

**Note**: This is an educational project for AltSchool's second semester examination. The in-memory storage is intentional for simplicity and demonstration purposes.

