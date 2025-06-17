from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.config.database import SessionDep
from app.schemas.event import EventCreate, EventUpdate
from app.models import Event, User, Registration


class EventService:
    """Service class for Event CRUD operations"""

    def __init__(self, session: SessionDep = SessionDep): # type: ignore
        self.session = session

    async def create_event(self, event_data: EventCreate) -> Event:
        """Create a new event"""
        event = Event(**event_data.model_dump())
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_event_by_id(self, event_id: int) -> Optional[Event]:
        """Get event by ID"""
        statement = select(Event).where(Event.event_id == event_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_all_events(self, skip: int = 0, limit: int = 100, open_only: bool = True) -> List[Event]:
        """Get all events with pagination"""
        statement = select(Event)
        if open_only:
            statement = statement.where(Event.event_is_open == True)
        statement = statement.offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_events_by_location(self, location: str) -> List[Event]:
        """Get events by location"""
        statement = select(Event).where(Event.event_location.ilike(f"%{location}%"))
        result = await self.session.exec(statement)
        return list(result.all())

    async def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        """Update event"""
        event = await self.get_event_by_id(event_id)
        if not event:
            return None
        
        event_data_dict = event_data.model_dump(exclude_unset=True)
        for key, value in event_data_dict.items():
            setattr(event, key, value)
        
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def delete_event(self, event_id: int) -> bool:
        """Delete event"""
        event = await self.get_event_by_id(event_id)
        if not event:
            return False
        
        event.event_is_open = False
        self.session.add(event)
        await self.session.commit()
        return True
    
    async def get_event_attendees(self, event_id: int) -> List[User]:
        """Get all attendees for an event"""
        statement = (
            select(User)
            .join(Registration)
            .where(Registration.event_id == event_id)
        )
        result = await self.session.exec(statement)
        return list(result.all())

    async def register_user_to_event(self, user_id: int, event_id: int) -> Registration:
        """Register a user to an event with validation"""
        
        # Check if user exists and is active
        user_statement = select(User).where(User.user_id == user_id)
        user = await self.session.exec(user_statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not user.user_is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only active users can register"
            )

        # Check if event exists and is open
        event_statement = select(Event).where(Event.event_id == event_id)
        event = await self.session.exec(event_statement).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        if not event.event_is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event must be open for registration"
            )

        # Check if user is already registered for this event
        existing_registration = select(Registration).where(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        )
        existing = await self.session.exec(existing_registration).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User cannot register more than once for the same event"
            )

        # Create registration
        try:
            registration = Registration(user_id=user_id, event_id=event_id)
            self.session.add(registration)
            await self.session.commit()
            await self.session.refresh(registration)
            return registration
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed"
            )

    async def mark_attendance(self, registration_id: int) -> Registration:
        """Mark attendance for a registration"""
        statement = select(Registration).where(Registration.registration_id == registration_id)
        registration = await self.session.exec(statement).first()
        
        if not registration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registration not found"
            )
        
        registration.user_attended = True
        self.session.add(registration)
        await self.session.commit()
        await self.session.refresh(registration)
        return registration

    async def get_user_registrations(self, user_id: int) -> List[Registration]:
        """Get all registrations for a specific user"""
        statement = select(Registration).where(Registration.user_id == user_id)
        result = await self.session.exec(statement)
        return list(result.all())

    async def get_all_registrations(self, skip: int = 0, limit: int = 100) -> List[Registration]:
        """Get all registrations with pagination"""
        statement = select(Registration).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return list(result.all())

