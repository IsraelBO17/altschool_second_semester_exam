from typing import List
from fastapi import APIRouter, Query, status
from app.services.event import EventService
from app.schemas.event import RegistrationResponse

router = APIRouter(prefix="/registrations", tags=["registrations"])
event_service = EventService()


@router.get("/", response_model=List[RegistrationResponse])
def get_all_registrations():
    """View all registrations"""
    registrations = event_service.get_all_registrations()
    return [RegistrationResponse.model_validate(registration) for registration in registrations]


@router.get("/user/{user_id}", response_model=List[RegistrationResponse])
def get_user_registrations(user_id: int):
    """View registrations for a specific user"""
    registrations = event_service.get_user_registrations(user_id)
    return [RegistrationResponse.model_validate(registration) for registration in registrations]


@router.post("/{event_id}/register/{user_id}", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_user_to_event(event_id: int, user_id: int):
    """Register a user to an event with validation"""
    registration = event_service.register_user_to_event(user_id, event_id)
    return RegistrationResponse.model_validate(registration)


@router.put("/{registration_id}/attendance", response_model=RegistrationResponse)
def mark_attendance(registration_id: int):
    """Mark attendance for a registration (set attended to True)"""
    registration = event_service.mark_attendance(registration_id)
    return RegistrationResponse.model_validate(registration)

