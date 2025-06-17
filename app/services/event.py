from typing import List, Optional
from datetime import date
from fastapi import HTTPException, status

from app.models import Event, User, Registration
from app.database import events, users, registrations
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    """Service class for Event CRUD operations"""

    def create_event(self, event_data: EventCreate) -> Event:
        """Create a new event"""
        # Generate new ID
        new_id = len(events) + 1
        
        event = Event(
            id=new_id,
            title=event_data.title,
            location=event_data.location,
            event_date=event_data.date,
        )
        events.append(event)
        return event

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        for event in events:
            if event.id == event_id:
                return event
        return None

    def get_all_events(self, open_only: bool = True) -> List[Event]:
        """Get all events"""
        if open_only:
            filtered_events = [e for e in events if e.is_open]
        else:
            filtered_events = events
        
        return filtered_events

    def get_events_by_location(self, location: str) -> List[Event]:
        """Get events by location"""
        return [event for event in events if location.lower() in event.location.lower()]

    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update event"""
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        
        # Update fields from schema
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.location is not None:
            event.location = event_data.location
        if event_data.date is not None:
            event.event_date = event_data.date
        
        return event

    def close_event(self, event_id: int) -> bool:
        """Close event (mark as closed)"""
        event = self.get_event_by_id(event_id)
        if not event:
            return False
        
        event.is_open = False
        return True
    
    def get_event_attendees(self, event_id: int) -> List[User]:
        """Get all attendees for an event"""
        event_registrations = [r for r in registrations if r.event_id == event_id]
        attendees = []
        
        for registration in event_registrations:
            for user in users:
                if user.id == registration.user_id:
                    attendees.append(user)
                    break
        
        return attendees

    def register_user_to_event(self, user_id: int, event_id: int) -> Registration:
        """Register a user to an event with validation"""
        
        # Check if user exists and is active
        user = None
        for u in users:
            if u.id == user_id:
                user = u
                break
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only active users can register"
            )

        # Check if event exists and is open
        event = self.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        if not event.is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event must be open for registration"
            )

        # Check if user is already registered
        for registration in registrations:
            if registration.user_id == user_id and registration.event_id == event_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User already registered for this event"
                )

        # Create registration
        new_id = len(registrations) + 1
        registration = Registration(
            id=new_id,
            user_id=user_id,
            event_id=event_id,
            registration_date=date.today()
        )
        registrations.append(registration)
        return registration

    def mark_attendance(self, registration_id: int) -> Registration:
        """Mark attendance for a registration"""
        for registration in registrations:
            if registration.id == registration_id:
                registration.attended = True
                return registration
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )

    def get_user_registrations(self, user_id: int) -> List[Registration]:
        """Get all registrations for a specific user"""
        return [r for r in registrations if r.user_id == user_id]

    def get_all_registrations(self) -> List[Registration]:
        """Get all registrations"""
        return registrations

