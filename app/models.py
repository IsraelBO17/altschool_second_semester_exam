from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from sqlalchemy.sql import func


class Registration(SQLModel, table=True):
    __tablename__ = "Registration"
    
    registration_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="User.user_id", ondelete="CASCADE")
    event_id: int = Field(index=True, foreign_key="Event.event_id", ondelete="CASCADE")
    registration_date: date = Field(sa_column_kwargs={"server_default": func.current_date()})
    user_attended: bool = Field(default=False, sa_column_kwargs={"server_default": "false"})


class User(SQLModel, table=True):
    __tablename__ = "User"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(max_length=255)
    user_email: EmailStr = Field(index=True, unique=True)
    user_is_active: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})

    # Relationship
    events: List["Event"] = Relationship(back_populates="attendees", link_model=Registration)


class Event(SQLModel, table=True):
    __tablename__ = "Event"

    event_id: Optional[int] = Field(default=None, primary_key=True)
    event_title: str = Field(max_length=255)
    event_location: str = Field(max_length=255)
    event_date: date = Field(sa_column_kwargs={"server_default": func.current_date()})
    event_is_open: bool = Field(default=True, sa_column_kwargs={"server_default": "true"})

    # Relationship
    attendees: List[User] = Relationship(back_populates="events", link_model=Registration)


class Speaker(SQLModel, table=True):
    __tablename__ = "Speaker"

    speaker_id: Optional[int] = Field(default=None, primary_key=True)
    speaker_name: str = Field(max_length=255)
    speaker_topic: str = Field(max_length=255)

