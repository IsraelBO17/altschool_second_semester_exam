from typing import Optional
from datetime import date
from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    location: str
    date: date


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    date: Optional[date] = None # type: ignore


class EventResponse(EventBase):
    id: int
    is_open: bool

    class Config:
        from_attributes = True


class RegistrationBase(BaseModel):
    user_id: int
    event_id: int


class RegistrationResponse(RegistrationBase):
    id: int
    registration_date: date
    attended: bool

    class Config:
        from_attributes = True

