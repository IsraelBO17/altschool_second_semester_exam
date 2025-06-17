from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.config.database import SessionDep
from app.services.event import EventService
from app.schemas.event import EventCreate, EventUpdate, EventResponse
from app.schemas.user import UserResponse


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    session: SessionDep = SessionDep  # type: ignore
):
    """Create a new event"""
    event_service = EventService(session)
    return await event_service.create_event(event_data)


@router.get("/", response_model=List[EventResponse])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    open_only: bool = Query(True),
    location: Optional[str] = Query(None),
    session: SessionDep = SessionDep  # type: ignore
):
    """Get all events with optional filtering"""
    event_service = EventService(session)
    
    if location:
        events = await event_service.get_events_by_location(location)
    else:
        events = await event_service.get_all_events(skip=skip, limit=limit, open_only=open_only)
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """Get event by ID"""
    event_service = EventService(session)
    event = await event_service.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return event


@router.get("/{event_id}/attendees", response_model=List[UserResponse])
async def get_event_attendees(
    event_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """Get all attendees for an event"""
    event_service = EventService(session)
    attendees = await event_service.get_event_attendees(event_id)
    return attendees


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    session: SessionDep = SessionDep  # type: ignore
):
    """Update event by ID"""
    event_service = EventService(session)
    updated_event = await event_service.update_event(event_id, event_data)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return updated_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """Delete event by ID (soft delete)"""
    event_service = EventService(session)
    success = await event_service.delete_event(event_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

