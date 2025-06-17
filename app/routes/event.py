from typing import List, Optional
from fastapi import APIRouter, HTTPException, Path, Query, status
from app.services.event import EventService
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix="/events", tags=["events"])
event_service = EventService()


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate):
    """Create a new event"""
    event = event_service.create_event(event_data)
    return EventResponse.model_validate(event)


@router.get("/", response_model=List[EventResponse])
def get_events(
    open_only: bool = Query(True),
    location: Optional[str] = Query(None)
):
    """Get all events with optional filtering"""
    if location:
        events = event_service.get_events_by_location(location)
    else:
        events = event_service.get_all_events(open_only=open_only)
    
    return [EventResponse.model_validate(event) for event in events]


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    """Get event by ID"""
    event = event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return EventResponse.model_validate(event)


@router.get("/{event_id}/attendees", response_model=List[UserResponse])
def get_event_attendees(event_id: int):
    """Get all attendees for an event"""
    # First check if event exists
    event = event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    attendees = event_service.get_event_attendees(event_id)
    return [UserResponse.model_validate(user) for user in attendees]


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventUpdate,
):
    """Update event by ID"""
    updated_event = event_service.update_event(event_id, event_data)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return EventResponse.model_validate(updated_event)


@router.put("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def close_event(event_id: int):
    """Close event by ID (soft delete - marks as closed)"""
    success = event_service.close_event(event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

