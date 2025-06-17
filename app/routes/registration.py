from typing import List
from fastapi import APIRouter, Query, status
from app.config.database import SessionDep
from app.services.event import EventService
from app.schemas.event import RegistrationResponse

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("/{event_id}/register/{user_id}", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_user_to_event(
    event_id: int,
    user_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """Register a user to an event with validation"""
    event_service = EventService(session)
    return await event_service.register_user_to_event(user_id, event_id)


@router.put("/{registration_id}/attendance", response_model=RegistrationResponse)
async def mark_attendance(
    registration_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """Mark attendance for a registration (set attended to True)"""
    event_service = EventService(session)
    return await event_service.mark_attendance(registration_id)


@router.get("/user/{user_id}", response_model=List[RegistrationResponse])
async def get_user_registrations(
    user_id: int,
    session: SessionDep = SessionDep  # type: ignore
):
    """View registrations for a specific user"""
    event_service = EventService(session)
    return await event_service.get_user_registrations(user_id)


@router.get("/", response_model=List[RegistrationResponse])
async def get_all_registrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: SessionDep = SessionDep  # type: ignore
):
    """View all registrations with pagination"""
    event_service = EventService(session)
    return await event_service.get_all_registrations(skip=skip, limit=limit)

