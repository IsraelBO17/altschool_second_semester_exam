from typing import Optional
from datetime import date
from pydantic import BaseModel


class EventBase(BaseModel):
    event_title: str
    event_location: str
    event_date: date


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    event_title: Optional[str] = None
    event_location: Optional[str] = None
    event_date: Optional[date] = None


class EventResponse(EventBase):
    event_id: int
    event_is_open: bool

    class Config:
        from_attributes = True


class RegistrationBase(BaseModel):
    user_id: int
    event_id: int


class RegistrationResponse(RegistrationBase):
    registration_id: int
    registration_date: date
    user_attended: bool

    class Config:
        from_attributes = True

